import os

import networkx as nx


class ReadLFR:

    def __init__(self, network_sizes, mixing_parameters, overlapping_fractions=''):
        self.network_sizes = network_sizes
        self.mixing_parameters = mixing_parameters
        self.overlapping_fractions = overlapping_fractions
        self.dir = os.path.dirname(__file__)
        self.prefix = ""
        if overlapping_fractions == '':
            self.prefix = "../../data/lfr/"
        else:
            self.prefix = "../../data/lfr/overlap_"

    def read(self):
        output = {}
        for size in self.network_sizes:
            for mix_param in self.mixing_parameters:
                if self.overlapping_fractions == '':
                    self.read_communities(size, mix_param, output)
                else:
                    for overlap in self.overlapping_fractions:
                        overlap_string = "%s_" % str(overlap)
                        self.read_communities(size, mix_param, output, overlap=overlap_string)

        return output

    def read_communities(self, size, mix_param, output, overlap=''):
        community = "%s%s_%s_%scommunity.dat" % (self.prefix, size, mix_param, overlap)
        network = "%s%s_%s_%snetwork.dat" % (self.prefix, size, mix_param, overlap)
        graph, communities = self.extract(network, community)
        if overlap == '':
            output[(size, mix_param)] = (graph, communities)
        else:
            overlap = overlap.strip('_')
            output[(size, mix_param, overlap)] = (graph, communities)



    def extract(self, network, community):
        G = nx.Graph()
        members = {}

        network = os.path.join(self.dir, network)
        community = os.path.join(self.dir, community)

        with open(network, 'rb') as f:
            for line in f:
                line = line.decode('utf-8').strip().split()
                vertex_from = line[0]
                vertex_to = line[1]
                G.add_edge(vertex_from, vertex_to)

        with open(community, 'rb') as f:
            for line in f:
                line = line.decode('utf-8').strip().split()
                vertex = line[0]
                for i in range(1, len(line)):
                    members.setdefault(vertex, [])
                    cluster_number = line[i]
                    members[vertex].append(cluster_number)

        return (G, members)

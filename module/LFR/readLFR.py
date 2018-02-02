import os

import networkx as nx


class readLFR:

    def __init__(self, network_sizes, mixing_parameters):
        self.network_sizes = network_sizes
        self.mixing_parameters = mixing_parameters
        self.dir = os.path.dirname(__file__)

    def read(self):
        output = {}
        for size in self.network_sizes:
            for mix_param in self.mixing_parameters:
                community = "../data/lfr/%s_%s_community.dat" % (size, mix_param)
                network = "../data/lfr/%s_%s_network.dat" % (size, mix_param)
                graph, communities = self.extract(network, community)
                output[(size, mix_param)] = (graph, communities)

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
                cluster_number = line[1]
                members[vertex] = cluster_number

        return (G, members)



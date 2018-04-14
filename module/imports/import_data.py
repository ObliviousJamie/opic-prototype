import os
import networkx as nx

from module.tools.extra.graph_clean import GraphClean


class ImportData:

    def __init__(self, call_location):
        self.dir = call_location

    def ground_truth_multiline(self, filename):
        location = os.path.join(self.dir, filename)
        communities = {}
        community_count = 0
        with open(location, 'rb') as f:
            data = f.readlines()

        for line in data:
            line = line.decode('utf-8').strip().split()
            for vertex in line:
                communities.setdefault(community_count,[]).append(vertex)
            community_count += 1
        return communities

    def text_graph(self, file_location):
        location = os.path.join(self.dir, file_location)
        end = file_location.split(".")[-1]

        fh = open(location, 'rb')

        if end == "net":
            graph = nx.read_pajek(fh)
        else:
            graph = nx.read_edgelist(fh)

        fh.close()

        cleaner = GraphClean()
        graph = cleaner.prune_unconnected_components(graph)
        return graph

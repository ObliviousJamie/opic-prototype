import os
import networkx as nx


class ImportData:

    def __init__(self):
        self.dir = os.path.dirname(__file__)

    def ground_truth(self, filename):
        location = os.path.join(self.dir, filename)
        communities = {}
        with open(location, 'rb') as f:
            data = f.readlines()

        for line in data:
            line = line.decode('utf-8').strip().split()
            vertex = line[0]
            community = line[1]
            # Add vertex to list of vertices in community
            communities.setdefault(community,[]).append(vertex)
        return communities

    def text_graph(self, file_location):
        location = os.path.join(self.dir, file_location)
        fh = open(location, 'rb')
        G = nx.read_edgelist(fh)
        fh.close()
        return G

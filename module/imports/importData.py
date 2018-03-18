import os
import networkx as nx


class ImportData:

    def __init__(self, call_location):
        self.dir = call_location

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
        print(file_location)
        location = os.path.join(self.dir, file_location)
        fh = open(location, 'rb')
        G = nx.read_edgelist(fh)
        fh.close()
        return G

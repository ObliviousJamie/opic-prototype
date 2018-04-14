import networkx as nx
from tqdm import tqdm

from module.lfr.helper import LFRHelper
from module.expansion.neighborhood import NeighborExpand
from module.expansion.ppr import PPR
from module.import_options import Options


class GMLWriter:

    def __init__(self, save_location, custom_seeders):
        self.save_location = save_location
        self.seeders = custom_seeders

    def lfr_to_gml(self, reader):
        for seeder in self.seeders:
            lfr_dict = reader.read()
            for key, value in lfr_dict.items():

                size, mix, overlap = LFRHelper.extract_key(key)

                graph, communities = value

                for vertex, membership in communities.items():
                    graph.node[vertex]['community'] = membership
                    graph.node[vertex]['roverlap'] = len(membership)

                if seeder:
                    found_communities = self.find_communities(seeder, graph)
                    for vertex, membership in found_communities.items():
                        graph.node[vertex]['bigdiscover'] = max(membership)
                        graph.node[vertex]['smalldiscover'] = min(membership)
                        graph.node[vertex]['foverlap'] = len(membership)

                loc = "%s_%s_%s_%s_%s.gml" % (self.save_location, size, mix, overlap, seeder.name)
                nx.write_gml(graph, loc)

    def graph_to_gml(self, graph, real_communities=None):
        clean_graph = graph.to_undirected()
        for seeder in self.seeders:
            graph = clean_graph.to_undirected()
            found_communities = self.find_communities(seeder, graph)
            for vertex, membership in found_communities.items():
                graph.node[vertex]['bigdiscover'] = max(membership)
                graph.node[vertex]['smalldiscover'] = min(membership)
                graph.node[vertex]['foverlap'] = len(membership)

            if real_communities is not None:
                for membership, vertices in real_communities.items():
                    for vertex in vertices:
                        graph.node[vertex]['community'] = membership

            loc = "%s_%s.gml" % (self.save_location, seeder.name)
            nx.write_gml(graph, loc)

    @staticmethod
    def find_communities(seeder, graph):
        ppr = PPR()
        communities = {}

        seeds = seeder.seed(graph)

        expander = NeighborExpand(graph)
        expanded_seeds = expander.expand_seeds(seeds)

        community_count = 0
        size_tuples = []

        for center_seed, neighbor_seeds in tqdm(expanded_seeds.items(), desc="Expanding seeds to form communities", unit="seed", total=len(seeds)):
            detected = ppr.ppr_rank(graph, neighbor_seeds)
            graph.node[center_seed]['cseed'] = str(community_count)
            for seed in neighbor_seeds:
                graph.node[seed]['nseed'] = str(community_count)

            if len(detected) > 2:
                size_tuples.append((len(detected), detected))
                community_count += 1

        community_count = 0
        size_tuples = sorted(size_tuples)
        for _, detected in size_tuples:
            for v in detected:
                communities.setdefault(v, [])
                communities[v].append(str(community_count))
        community_count += 1

        return communities


if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv, parameters="smocdt")
    seeders = option_import.select_seeders()

    directory = os.getcwd()
    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/network{date}"

    reader = option_import.generate_reader()
    gml_writer = GMLWriter(save_name, seeders)

    if reader is not None:
        gml_writer.lfr_to_gml(reader)
    else:
        graph, communities = option_import.import_real(directory, need_truth=False)
        print("Graph and community imported")
        gml_writer.graph_to_gml(graph, communities)




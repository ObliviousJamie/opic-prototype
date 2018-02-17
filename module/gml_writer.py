import networkx as nx

from module.LFR.readLFR import readLFR
from module.PPR import PPR
from module.seeding.mfc_min_seed import SeedMinMFC
from module.seeding.mfc_opic_seed import SeedMFCOPIC
from module.seeding.opic_seed import SeedOPIC
from module.seeding.spreadhub_seed import Spreadhub


def lfr_to_gml(reader, save_location, seeder=None):
    lfr_dict = reader.read()
    for key, value in lfr_dict.items():
        size, mix, overlap = key
        graph, communities = value

        for vertex, membership in communities.items():
            graph.node[vertex]['community'] = membership

        if seeder:
            found_communities = find_communities(seeder, graph)
            for vertex, membership in found_communities.items():
                graph.node[vertex]['discover'] = membership

        loc = "%s_%s_%s_%s.gml" % (save_location, size, mix, overlap)
        nx.write_gml(graph, loc)


def ground_to_gml():
    pass


def find_communities(seeder, graph):
    print("Seeding...")
    seeds = seeder.seed(graph)
    print("Seeds", len(seeds))
    print("Seeds generated")
    ppr = PPR(graph)
    used_seeds = set()
    communities = {}
    community_count = 0

    for seed in seeds:
        expanded_seeds = set()
        if seed not in used_seeds:
            expanded_seeds.add(seed)
            graph.node[seed]['seed'] = str(community_count)
        for v in graph[seed]:
            if v not in used_seeds:
                #expanded_seeds.add(v)
                used_seeds.add(v)
                #graph.node[v]['seed'] = str(community_count)
        print(expanded_seeds)

        if len(expanded_seeds) > 0:
            # TODO change tol
            bestset = ppr.PPRRank(graph, 0.99, 0.0001, expanded_seeds)
            # TODO sensitivity test
            if len(bestset) > 2:
                for vertex in bestset:
                    communities.setdefault(vertex, [])
                    communities[vertex].append(str(community_count))

            community_count += 1

    return communities


opic = SeedOPIC(1.8, return_type='string')
mfc_min = SeedMinMFC(3.0, return_type='string')
mfc_opic = SeedMFCOPIC(2.8, return_type='string')
spreadhub = Spreadhub(35)

reader = readLFR([1000], [0.1, 0.3], overlapping_fractions=[0.1, 0.2, 0.3, 0.4, 0.5])
#reader = readLFR([50000], [0.1], overlapping_fractions=[0.1, 0.5])
# TODO make work with find_communities
#print("OPIC")
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/opic_attributes_graph', opic)
#print("MFC OPIC")
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/mfcopic_attributes_graph', mfc_opic)
#print("MFC MIN")
lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/mfc_min_attributes_graph', mfc_min)
exit()
print("Spreadhub")
lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/spreadhub_attributes_graph', spreadhub)

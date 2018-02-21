import networkx as nx

from module.LFR.readLFR import readLFR
from module.expansion.PPR import PPR
from module.seeding.mfc_min_seed import SeedMinMFC
from module.seeding.mfc_minhub_seed import SeedMinhubMFC
from module.seeding.mfc_opic_seed import SeedMFCOPIC
from module.seeding.opic_seed import SeedOPIC
from module.seeding.opichub_seed import SeedOPICHub
from module.seeding.seed_filter import DefaultFilter
from module.seeding.spreadhub_seed import Spreadhub


def lfr_to_gml(reader, save_location, seeder=None):
    lfr_dict = reader.read()
    for key, value in lfr_dict.items():
        size, mix, overlap = key
        graph, communities = value

        for vertex, membership in communities.items():
            graph.node[vertex]['community'] = membership
            graph.node[vertex]['roverlap'] = len(membership)

        if seeder:
            found_communities = find_communities(seeder, graph)
            for vertex, membership in found_communities.items():
                graph.node[vertex]['discover'] = membership
                graph.node[vertex]['rdiscover'] = membership[::-1]
                graph.node[vertex]['foverlap'] = len(membership)

        loc = "%s_%s_%s_%s.gml" % (save_location, size, mix, overlap)
        nx.write_gml(graph, loc)


def ground_to_gml():
    pass


def find_communities(seeder, graph):
    print("Seeding...")
    seeds = seeder.seed(graph)
    #print("Seeds", len(seeds))
    print("Seeds generated")
    ppr = PPR(graph)
    used_seeds = set()
    communities = {}
    community_count = 0
    total_seeds = 0

    for seed in seeds:
        expanded_seeds = set()
        if seed not in used_seeds:
            expanded_seeds.add(seed)
            graph.node[seed]['cseed'] = str(community_count)
            neighbors = (list(graph.neighbors(seed)))
            for v in neighbors:
                if v not in used_seeds:
                    expanded_seeds.add(v)
                    used_seeds.add(v)
                    graph.node[v]['nseed'] = str(community_count)

        if len(expanded_seeds) > 0:
            total_seeds +=1
            # TODO change tol
            bestset = ppr.PPRRank(graph, 0.99, 0.0001, expanded_seeds)
            # TODO sensitivity test
            if len(bestset) > 2:
                for vertex in bestset:
                    communities.setdefault(vertex, [])
                    communities[vertex].append(str(community_count))

            community_count += 1
    print("Total seeds", total_seeds)
    if total_seeds > 0.1 * len(list(graph.nodes)):
        print("killed")
        exit()

    return communities


opic = SeedOPIC(1.6, start='1', return_type='string')
mfc_min = SeedMinMFC(2.6, start='1',  return_type='string')
mfc_min_f = SeedMinMFC(2.6, start='1',  return_type='string', s_filter=DefaultFilter())
mfc_opic = SeedMFCOPIC(1.6, start='1', return_type='string')

spreadhub = Spreadhub(35)
mfc_minhub = SeedMinhubMFC(40, '1')
opichub = SeedOPICHub(40, '1')

#reader = readLFR([1000], [0.1, 0.3], overlapping_fractions=[0.1, 0.2, 0.3, 0.4, 0.5])
reader = readLFR([1000], [0.1, 0.3], overlapping_fractions=[0.1, 0.3])
#reader = readLFR([50000], [0.1], overlapping_fractions=[0.1, 0.5])
# TODO make work with find_communities
#print("OPIC")
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/opic_attributes_graph', opic)
#print("MFC OPIC")
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/mfcopic_attributes_graph', mfc_opic)
#print("MFC MIN")
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/mfc_min_attributes_graph', mfc_min)
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/mfchub_attributes_graph', mfc_minhub)
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/opichub_attributes_graph', opichub)
#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/spreadhub_attributes_graph', spreadhub)


#lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/m_mfc_min_attributes_graph', mfc_min)
lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/f_mfc_min_attributes_graph', mfc_min_f)


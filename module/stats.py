import networkx as nx

from module.LFR.plotLFR import PlotLFR
from module.LFR.readLFR import ReadLFR
from module.LFR.WriteLFR import WriteLFR
from module.graph.tools.expand_seeds import SeedExpansion
from module.graph.tools.graph_clean import GraphClean
from module.imports.importData import ImportData
from module.seeder import Seeder
from module.statistics.accuracy import Stats


def community_stats(ground_truth_communities, found):
    stats = Stats(ground_truth_communities)
    mean = stats.compare(found)

    print("Mean accuracy %f" % mean)
    print("Communities detected %s" % len(found))
    print("Real Communities %s" % len(ground_truth_communities))


def karate(seeder):
    K = nx.karate_club_graph()
    seeds = seeder.seed(K)
    expander = SeedExpansion()

    discovered_communities = expander.expand(seeds, K, tol=0.01, use_neighborhood=True)

    for key, value in discovered_communities.items():
        print("Seed: %s found:  %s" % (key, value))


def imported(import_path, seeder, ground_truth=''):
    imports = ImportData()
    cleaner = GraphClean()
    I = imports.text_graph(import_path)
    I = cleaner.prune_unconnected_components(I)
    expander = SeedExpansion()

    seeds = seeder.seed(I)

    discovered_communities = expander.expand(seeds, I)

    if ground_truth != '':
        real_communities = imports.ground_truth(ground_truth)
        community_stats(real_communities, discovered_communities)
    else:
        size = 0
        for key, value in discovered_communities.items():
            print("Seed: %s found:  %s" % (key, value))
            size += len(value)

        discovered_length = len(discovered_communities.keys())
        average_size = size / discovered_length
        print("Communities discovered: %s" % discovered_length)
        print("Average community size %s" % average_size)




def flip_list_dict(dictionary):
    new_dict = {}
    for key, value_list in dictionary.items():
        for item in value_list:
            new_dict.setdefault(item, list())
            new_dict[item].append(key)
    return new_dict




# Built in graphs


reader = ReadLFR([1000], [0.1, 0.3], overlapping_fractions=[0.1, 0.2, 0.3, 0.4, 0.5])

# Imported Graphs

# imported('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core', threshold=2.7)

# import_coverage('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core', threshold=2.7)

# K = nx.karate_club_graph()


# Coverage

#reader = readLFR([5000, 50000], [0.1, 0.3], overlapping_fractions=[0.1, 0.2, 0.3, 0.4, 0.5])

#graph = nx.karate_club_graph()
#
#
#reader = readLFR([5000, 50000], [0.1, 0.3], overlapping_fractions=[0.1, 0.3, 0.5])
#
#imports = ImportData()
#I = imports.text_graph('../data/edgelist/eu-core')
#
#I = prune_unconnected_components(I)
#

#real_communities = imports.ground_truth('../data/ground-truth/eu-core')
#membership = flip_list_dict(real_communities)
#
#print(real_communities)
#print(membership)
#

#crawl = CrawlStats()
#crawl.coverage_plot(I, real_communities, membership)

# eu = '../data/edgelist/eu-core'
# eu_truth = '../data/ground-truth/eu-core'
#
# dblp = '../data/edgelist/dblp'
# dblp_truth = '../data/ground-truth/dblp'
# dblp_truth_min = '../data/ground-truth/dblp_5000'
#
# imports = ImportData()
# I = imports.text_graph(eu)
#
# I = prune_unconnected_components(I)
#
# real_communities = imports.ground_truth(eu_truth)
# membership = flip_list_dict(real_communities)

# print(len(real_communities))
# print(len(membership))
#
#
# crawl = CrawlStats()
# crawl.coverage_plot(I, real_communities, membership)
# imported('../data/edgelist/hepph-phenomenology', '17010', threshold=1.4)
# benchmark_graph = LFR_benchmark_graph(1000,3,1.5,0.1, average_degree=30, min_community=50)

# reader = readLFR([1000,5000],[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8])
# lfr = plotLFR(reader, Seeder())
# lfr.compute_communities()

# lfr = plotLFR(reader, Seeder())
# lfr.compute_communities(1.62)


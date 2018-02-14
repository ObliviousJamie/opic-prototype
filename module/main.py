from random import choice

import matplotlib.pyplot as plt
import networkx as nx

from module.LFR.plotLFR import plotLFR
from module.LFR.readLFR import readLFR
from module.LFR.writeLFR import writeLFR
from module.PPR import PPR
from module.coverage_plot import Coverage
from module.importData import ImportData
from module.seeder import Seeder
from module.stats import Stats


def calculate_seeds(seeds, G, tol=0.0001, should_draw=True, is_large=False, use_neighborhood=True):
    pos = nx.spring_layout(G)

    ppr = PPR(G)

    community = {}
    index = 0
    for seed in seeds:
        seed_array = G[seed] if use_neighborhood else [seed]
        best = ppr.PPRRank(G, 0.99, tol, seed_array)
        community[seed] = best

        if should_draw and is_large:
            nx.draw_networkx_nodes(G, pos, best, node_size=10)
        elif should_draw:
            color = 'C' + str(index % 8)
            nx.draw_networkx_nodes(G, pos, best, node_color=color, node_size=150)
            index += 1

    if should_draw and is_large:
        nx.draw_networkx_edges(G, pos, width=0.05, color='grey')
        plt.show()
    elif should_draw:
        nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
        nx.draw_networkx_edges(G, pos, width=0.5, color='grey')
        plt.show()

    return community


def community_stats(ground_truth_communities, found):
    stats = Stats(ground_truth_communities)
    mean = stats.compare(found)

    print("Mean accuracy %f" % mean)
    print("Communities detected %s" % len(found))
    print("Real Communities %s" % len(ground_truth_communities))


def karate(mfc=True):
    K = nx.karate_club_graph()
    seeder = Seeder()
    if mfc:
        seeds = seeder.seed_MFC_rank(K, 31, 1.6, True, return_type="integer", print_ranks=True)
    else:
        seeds = seeder.seed(K, 31, 1.6, True, return_type="integer", print_ranks=True)

    discovered_communities = calculate_seeds(seeds, K, tol=0.01, use_neighborhood=True)

    for key, value in discovered_communities.items():
        print("Seed: %s found:  %s" % (key, value))


def imported(import_path, start, ground_truth='', threshold=1.0, mfc=True):
    imports = ImportData()
    I = imports.text_graph(import_path)
    I = prune_unconnected_components(I)

    seeder = Seeder()
    if mfc:
        seeds = seeder.seed_MFC_rank(I, start, threshold, True, return_type="string", print_ranks=False)
    else:
        seeds = seeder.seed(I, start, threshold, True, return_type="string", print_ranks=False)

    discovered_communities = calculate_seeds(seeds, I, is_large=True, should_draw=False)

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


def plot_coverages(graph, seed_dict):
    plt.xlabel("% Coverage")
    plt.ylabel("Maximum Conductance")
    plt.axis([0, 105, 0, 1.01])
    print(seed_dict.keys())
    for label, seeds in seed_dict.items():
        print(label, len(seeds))
        if label == 'mfc-original':
            Coverage(graph, seeds).plot_coverage_mfc()
        else:
            Coverage(graph, seeds).plot_coverage(label)
    plt.legend()


def plot_multicoverage(import_path='', graph=''):
    if import_path != '':
        imports = ImportData()
        I = imports.text_graph(import_path)
        graph = prune_unconnected_components(I)
    seed_dict = {}

    start = choice(list(graph.nodes))

    seeder = Seeder()

    print("Processing MFC low seed")
    mfc_seed_low = seeder.seed_MFC_rank(graph, start, 2.4, False, return_type="string", print_ranks=False)

    # print("Processing OPIC low seed")
    # opic_seed_low = seeder.seed(graph, start, 1.8, False, return_type="string", print_ranks=False)

    print("Processing MFC ref")
    mfc_ref = seeder.seed_MFC(graph, start, 2.28, False, return_type="string", min=True)

    print("Processing spreadhub")
    limit = len(graph.nodes) * .2
    spreadhub = seeder.spreadhub(graph, int(limit))


    print("Processing MFC low seed")
    seed_dict["mfc_with_opic"] = mfc_seed_low
    seed_dict["mfc-min-peaks"] = mfc_ref
    seed_dict["speadhub"] = spreadhub

    print("Plotting graph...")
    plot_coverages(graph, seed_dict)


def flip_list_dict(dictionary):
    new_dict = {}
    for key, value_list in dictionary.items():
        for item in value_list:
            new_dict.setdefault(item, list())
            new_dict[item].append(key)
    return new_dict


def prune_unconnected_components(graph):
    current = graph
    # Remove self loops
    for vertex in graph.nodes_with_selfloops():
        graph.remove_edge(vertex, vertex)

    if not nx.is_connected(graph):
        connected_subgraphs = nx.connected_component_subgraphs(graph)
        current = next(connected_subgraphs)

        for sub_graph in connected_subgraphs:
            if len(sub_graph.nodes) > len(current.nodes):
                current = sub_graph
    return current


# Built in graphs


reader = readLFR([50000],[0.1,0.3], overlapping_fractions=[0.1,0.2,0.3,0.4,0.5])

# Imported Graphs

# imported('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core', threshold=2.7)

# import_coverage('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core', threshold=2.7)

# K = nx.karate_club_graph()
#lfr_dict = reader.read()
#for key, value in lfr_dict.items():
#   print(key)
#   size, mix, overlap = key
#   graph, _ = value
#   plot_multicoverage(graph= graph)
#   save_loc = "/home/jmoreland/Pictures/PRJ/coverage_%s_%s_%s_spread.png" % (size, mix, overlap)
#   print(save_loc)
#   plt.savefig(save_loc)
#   plt.close()
#

#plot_multicoverage('../data/edgelist/eu-core')
# plot_multicoverage('../data/edgelist/dblp')
# plot_multicoverage(graph=K)

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
#crawl = CrawlStats()
#
#lfr_dict = reader.read()
#for key, value in lfr_dict.items():
#    reverse = {}
#    graph, community = value
#    for vertex, members in community.items():
#        for community_key in members:
#            reverse.setdefault(community_key, [])
#            reverse[community_key].append(vertex)
#    print()
#    print()
#    print(key)
#    crawl = CrawlStats()
#    crawl.coverage_plot(graph, reverse, community)
#
    #crawl.coverage_plot(I, real_communities, membership)

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

#reader = readLFR([1000,5000],[0.1,0.3], overlapping_fractions=[0.1,0.2,0.3,0.4,0.5])
# lfr = plotLFR(reader, Seeder())
# lfr.compute_communities(1.62)

lfr2 = writeLFR(reader, Seeder())
#lfr2 = writeLFR(reader, Seeder(), write_truth=True)
lfr2.calculate_communities(2.0, method='mfcrank')
# lfr2.calculate_communities(1.6, method='opic')
lfr2.calculate_communities(0.8, method='mfcseed')
#lfr2.calculate_communities(0, method='spreadhub')
# lfr.save(2.0)

#lfr_plot = plotLFR([('mfcrank', '2.0'),('opic','1.6'),('mfcseed', '0.8'), ('spreadhub', '0')], save_loc="/home/jmoreland/Pictures/PRJ")
lfr_plot = plotLFR([('mfcrank', '2.0'),('mfcseed', '0.8'), ('spreadhub', '0')], save_loc="/home/jmoreland/Pictures/PRJ")
#lfr_plot = plotLFR([ ('spreadhub', '0')], save_loc="/home/jmoreland/Pictures/PRJ")
lfr_plot.plot([50000],[0.1,0.3],[0.1, 0.2, 0.3, 0.4, 0.5])

from random import choice

import matplotlib.pyplot as plt
import networkx as nx
from module.PPR import PPR
from module.coverage_plot import Coverage
from module.crawlStats import CrawlStats
from module.importData import ImportData
from module.seeder import Seeder
from module.stats import Stats
from networkx.algorithms.community import LFR_benchmark_graph


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
    # seeds = seeder.seed(K, 31, 1.6, True, return_type="integer", print_ranks=True)
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
    plt.axis([0, 100, 0, 1])
    print(seed_dict.keys())
    for label, seeds in seed_dict.items():
        print(label, len(seeds))
        Coverage(graph, seeds).plot_coverage(label)
    plt.legend()
    plt.show()


def plot_multicoverage(import_path='', graph=''):
    if import_path != '':
        imports = ImportData()
        I = imports.text_graph(import_path)
        graph = prune_unconnected_components(I)
    seed_dict = {}

    start = choice(list(graph.nodes))

    seeder = Seeder()


    print("Processing MFC low seed")
    mfc_seed_low = seeder.seed_MFC_rank(graph, start, 2.98, False, return_type="string", print_ranks=False)
    #mfc_seed_high = seeder.seed_MFC_rank(graph, start, 3.45, False, return_type="string", print_ranks=False)

    print("Processing OPIC low seed")
    opic_seed_low = seeder.seed(graph, start, 1.43, False, return_type="string", print_ranks=False)
    #opic_seed_high = seeder.seed(graph, start, 1.58, False, return_type="string", print_ranks=False)

    print("Processing MFC ref")
    mfc_ref = seeder.seed_MFC(graph, start, 0.8, False, return_type="string", print_ranks=False)

    random_small = []
    random_large = []

    print("Picking random")
    iterations = len(graph.nodes) / 20
    for i in range(int(iterations)):
        rnd = choice(list(graph.nodes))
        if i <= 30:
            random_small.append(rnd)
        random_large.append(rnd)

    print("Processing MFC low seed")
    seed_dict["mfc-seed-low-thres"] = mfc_seed_low
    #seed_dict["mfc-seed-high-thres"] = mfc_seed_high
    print("Processing OPIC low seed")
    seed_dict["opic-seed-low-thres"] = opic_seed_low
    #seed_dict["opic-seed-high-thres"] = opic_seed_high
    #seed_dict["random_small"] = random_small
    print("Processing random")
    seed_dict["random_large"] = random_large

    seed_dict["mfc-ref"] = mfc_ref

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
    #print("Degree", graph.degree('653'))
    #print("Degree", graph['653'])
    #print("Edges", graph.edges('653'))
    #print("Adj", graph.adj['653'])

    #print()
    #print("Degree", graph.degree('651'))
    #print("Degree", graph['651'])
    #print("Edges", graph.edges('651'))
    #print("Adj", graph.adj['651'])
    #print(list(graph.nodes_with_selfloops()))

    #Remove self loops
    for vertex in graph.nodes_with_selfloops():
        graph.remove_edge(vertex,vertex)

    if not nx.is_connected(graph):
        connected_subgraphs = nx.connected_component_subgraphs(graph)
        current = next(connected_subgraphs)

        for sub_graph in connected_subgraphs:
            if len(sub_graph.nodes) > len(current.nodes):
                current = sub_graph
    return current


# Built in graphs

# karate()


# Imported Graphs

#imported('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core', threshold=2.7)

#import_coverage('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core', threshold=2.7)

#K = nx.karate_club_graph()
plot_multicoverage('../data/edgelist/eu-core')
#plot_multicoverage('../data/edgelist/dblp')
#plot_multicoverage(graph=K)

# Coverage

# imports = ImportData()
# I = imports.text_graph('../data/edgelist/eu-core')
#
# I = prune_unconnected_components(I)
#
# real_communities = imports.ground_truth('../data/ground-truth/eu-core')
# membership = flip_list_dict(real_communities)

# crawl = CrawlStats()
# crawl.coverage_plot(I, real_communities, membership)
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

# n = 2501
# tau1 = 3
# tau2 = 1.5
# mu = 0.1
# G = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=5,
#                        min_community=20, seed=10)
# communities = {frozenset(G.nodes[v]['community']) for v in G}
# print(communities)

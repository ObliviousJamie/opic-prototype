import matplotlib.pyplot as plt
import networkx as nx
from module.PPR import PPR
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


def karate():
    K = nx.karate_club_graph()
    seeder = Seeder()
    seeds = seeder.seed(K, 31, 1.6, True, return_type="integer", print_ranks=True)
    discovered_communities = calculate_seeds(seeds, K, tol=0.01, use_neighborhood=True)

    for key, value in discovered_communities.items():
        print("Seed: %s found:  %s" % (key, value))


def imported(import_path, start, ground_truth='', threshold=1.0):
    imports = ImportData()
    I = imports.text_graph(import_path)

    seeder = Seeder()
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


def similar_communities():
    """ Finds arrays that are similar and returns them as a hash table
    This is used to discover similar seeds
    """
    pass


#Built in graphs

#karate()


# Imported Graphs

#imported('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core', threshold=1.4)
imported('../data/edgelist/hepph-phenomenology', '17010', threshold=1.4)

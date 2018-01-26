import matplotlib.pyplot as plt
import networkx as nx
from module.PPR import PPR
from module.importData import ImportData
from module.seeder import Seeder
from module.stats import Stats


def calculate_seeds(seeds, G, should_draw=True):
    options = {
        'node_size': 10,
        'line_color': 'grey',
        'linewidths': 0,
        'width': 0.05,
    }

    pos = nx.spring_layout(G)

    ppr = PPR(G)

    community = {}
    index = 0
    for seed in seeds:
        best = ppr.PPRRank(G, 0.99, 0.01, [seed])
        community[seed] = best
        if should_draw:
            color = 'C' + str(index % 8)
            nx.draw_networkx_nodes(G, pos, best, node_color=color, node_size=150)
            index += 1

    if should_draw:
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
    seeds = seeder.seed(K, 31, 1.6, True, return_type="integer")
    discovered_communities = calculate_seeds(seeds, K)

    for key, value in discovered_communities.items():
        print("Seed: %s found:  %s" % (key, value))


def imported(import_path, start, ground_truth='', threshold=1.0):
    imports = ImportData()
    I = imports.text_graph(import_path)

    seeder = Seeder()
    seeds = seeder.seed(I, start, threshold, True, return_type="string")

    print("Found: %s " % seeds)
    discovered_communities = calculate_seeds(seeds, I)
    print("Found: %s " % discovered_communities)

    if ground_truth != '':
        real_communities = imports.ground_truth(ground_truth)
        community_stats(real_communities, discovered_communities)


def similar_communities():
    """ Finds arrays that are similar and returns them as a hash table
    This is used to discover similar seeds
    """
    pass


karate()

exit()

# Imported Graphs

imported('../data/edgelist/eu-core', '7', ground_truth='../data/ground-truth/eu-core')

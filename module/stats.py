from module.graph.tools.expand_seeds import SeedExpansion
from module.graph.tools.graph_clean import GraphClean
from module.imports.importData import ImportData
from module.statistics.accuracy import Stats


def community_stats(ground_truth_communities, found):
    stats = Stats(ground_truth_communities)
    mean = stats.compare(found)

    print("Mean accuracy %f" % mean)
    print("Communities detected %s" % len(found))
    print("Real Communities %s" % len(ground_truth_communities))


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


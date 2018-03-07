from module.LFR.plotFscore import PlotFscore
from module.LFR.readLFR import ReadLFR
from module.graph.tools.expand_seeds import SeedExpansion
from module.graph.tools.graph_clean import GraphClean
from module.graph.tools.samples import Samples
from module.imports.importData import ImportData
from module.statistics.accuracy import Stats
from module.statistics.fscore import FScore


def community_stats(ground_truth_communities, found):
    stats = Stats(ground_truth_communities)
    mean = stats.compare(found)

    print("Mean accuracy %f" % mean)
    print("Communities detected %s" % len(found))
    print("Real Communities %s" % len(ground_truth_communities))


def fscores(real, found):
    fscore = FScore(real, found)
    f1 = fscore.f1()
    f2 = fscore.f2()
    return f1, f2


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


def lfr_fscores(reader, seeders):
    lfr_dict = reader.read()
    expander = SeedExpansion()
    for key, value in lfr_dict.items():
        size, mix, overlap = key
        graph, communities = value

        real_communities = {}
        for vertex, community in communities.items():
            for single_community in community:
                real_communities.setdefault(single_community, [])
                real_communities[single_community].append(vertex)

        print(real_communities)
        for seeder in seeders:
            seeds = seeder.seed(graph)
            found = expander.expand(seeds, graph)
            f1, f2 = fscores(real_communities, found)
            print()
            print(f"Seeder: {seeder.name}")
            print(f"F1: {f1}    F2: {f2}")
            print(f"Size {size}, Mix: {mix}, Overlap: {overlap}")
            print()


reader = ReadLFR([1000], [0.1], overlapping_fractions=[0.1])

ppr = Samples().seeders('ppr')
mfcopic = Samples().mfcopic_peak_variety(2.0, 0.5)

#lfr_fscores(reader, mfcopic)
save = '/home/jmoreland/Documents/PRJ/sensitivity/thres'
plotter = PlotFscore(mfcopic)
plotter.lfr_fscores(reader, f"{save}/threshold_variance.csv")



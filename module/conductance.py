import matplotlib.pyplot as plt

from module.LFR.readLFR import ReadLFR
from module.graph.tools.graph_clean import GraphClean
from module.graph.tools.samples import Samples
from module.imports.importData import ImportData
from module.statistics.coverage_plot import ConductancePlot


def plot_coverages(graph, seed_dict):
    plt.xlabel("% Coverage")
    plt.ylabel("Maximum Conductance")
    plt.axis([0, 105, 0, 1.01])
    print(seed_dict.keys())
    for label, seeds in seed_dict.items():
        print(label, len(seeds))
        if label == 'mfc-original':
            ConductancePlot(graph, seeds).plot_coverage_mfc()
        else:
            ConductancePlot(graph, seeds).plot_coverage(label)
    plt.legend()
    plt.show()


def plot_multicoverage(seeders, import_path='', graph=''):
    clean = GraphClean()
    if import_path != '':
        imports = ImportData()
        I = imports.text_graph(import_path)
        graph = clean.prune_unconnected_components(I)
    seed_dict = {}

    for seeder in seeders:
        print("Processing", seeder.name)
        seeds = seeder.seed(graph)
        seed_dict[seeder.name] = seeds

    print("Plotting graph...")
    plot_coverages(graph, seed_dict)

def plot_with_lfr(seeders, label=''):
    reader = ReadLFR([1000], [0.1, 0.3], overlapping_fractions=[0.1, 0.2, 0.3, 0.4, 0.5])
    lfr_dict = reader.read()
    for key, value in lfr_dict.items():
        print(key)
        size, mix, overlap = key
        graph, _ = value
        plot_multicoverage(seeders, graph= graph)
        save_loc = "/home/jmoreland/Pictures/PRJ/conductance_%s_%s_%s_%s_spread.png" % (label, size, mix, overlap)
        print(save_loc)
        plt.savefig(save_loc)
        plt.close()


seeders_norm = Samples().seeders('normal')
seeders_ppr = Samples().seeders('ppr')
seeders_neighbor = Samples().seeders('neighbor')

#plot_with_lfr(seeders_norm)
#plot_with_lfr(seeders_ppr, 'ppr')
#plot_with_lfr(seeders_neighbor, 'neighbor')

seeders_opic = Samples().seeders_mix('opic')
seeders_mfcopic = Samples().seeders_mix('mfcopic')
seeders_mfcmin = Samples().seeders_mix('mfcmin')

#plot_with_lfr(seeders_opic, 'opic')
#plot_with_lfr(seeders_mfcopic, 'mfcopic')
#plot_with_lfr(seeders_mfcmin, 'mfcmin')
print('Real graph')

plot_multicoverage(seeders_norm, '../../data/edgelist/eu-core')
plot_multicoverage(seeders_mfcopic, '../../data/edgelist/eu-core')
plot_multicoverage(seeders_ppr, '../../data/edgelist/eu-core')
# plot_multicoverage('../data/edgelist/dblp')
# plot_multicoverage(graph=K)


import matplotlib.pyplot as plt

from module.graph.tools.graph_clean import GraphClean
from module.imports.importData import ImportData
from module.statistics.coverage_plot import Coverage


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

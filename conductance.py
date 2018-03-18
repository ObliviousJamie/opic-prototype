import matplotlib.pyplot as plt

from module.import_options import Options
from module.statistics.coverage_plot import ConductancePlot


class ConductancePlotManager:

    def __init__(self, seeders, save_location):
        self.seeders = seeders
        self.save_base = save_location

    def plot_coverages(self, graph, seed_dict):
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

    def plot_multicoverage(self, graph, save_name):
        seed_dict = {}

        for seeder in self.seeders:
            print("Processing", seeder.name)
            seeds = seeder.seed(graph)
            seed_dict[seeder.name] = seeds

        print("Plotting graph...")
        self.plot_coverages(graph, seed_dict)
        if save_name != '':
            plt.savefig(save_name)
        plt.close()

    def plot_with_lfr(self, reader, label='LFR'):
        lfr_dict = reader.read()
        for key, value in lfr_dict.items():
            print(key)
            size, mix, overlap = key
            graph, _ = value
            save_loc = f"{self.save_base}_%s_%s_%s_%s_spread.png" % (label, size, mix, overlap)
            self.plot_multicoverage(graph=graph, save_name=save_loc)

if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv)
    seeders = option_import.select_seeders()

    directory = os.getcwd()

    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/conductance_{date}"

    conductanceMan = ConductancePlotManager(seeders, save_name)

    reader = option_import.generate_reader()
    if reader is not None:
        conductanceMan.plot_with_lfr(reader)
    else:
        graph, _ = option_import.import_real(directory)
        print("Graph and community imported")
        save_name = f"{directory}/conductance_{date}_real.png"
        conductanceMan.plot_multicoverage(graph, save_name)


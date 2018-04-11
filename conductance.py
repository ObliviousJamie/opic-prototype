import matplotlib.pyplot as plt
from module.LFR.helper import LFRHelper
from module.import_options import Options
from module.seeding.seeder.spreadhub import Spreadhub
from module.statistics.plots.coverage_plot import ConductancePlot


class ConductancePlotManager:

    def __init__(self, seeders, save_location):
        self.seeders = seeders
        self.save_base = save_location

    def plot_coverages(self, graph, seed_dict):
        plt.xlabel("% Coverage")
        plt.ylabel("Maximum Conductance")
        plt.axis([0, 105, 0, 1.01])

        cplot = ConductancePlot(graph)

        for label, seeds in seed_dict.items():
            print(label, len(seeds))
            cplot.plot_coverage(seeds, label)

        cplot.plot_coverage_mfc()

        spread = Spreadhub(int(0.15 * len(graph.nodes)))
        cplot.plot_coverage(spread.seed(graph), "Spreadhub")

        self._plot_labels()

    def plot_multicoverage(self, graph, save_name):
        seed_dict = {}

        for seeder in self.seeders:
            print("Processing...", seeder.name)
            seeds = seeder.seed(graph)

            seed_dict[seeder.name] = seeds

        self.plot_coverages(graph, seed_dict)
        if save_name != '':
            plt.savefig(save_name)
        plt.close()

    def plot_with_lfr(self, reader, label='LFR'):
        lfr_dict = reader.read()
        for key, value in lfr_dict.items():
            size, mix, overlap = LFRHelper.extract_key(key)

            graph, _ = value
            save_loc = f"{self.save_base}_%s_%s_%s_%s.png" % (label, size, mix, overlap)
            plt.title(f"Size: {size} Mix: {mix} Overlap {overlap}")
            self.plot_multicoverage(graph=graph, save_name=save_loc)

    @staticmethod
    def _plot_labels():
        plt.xlabel("% Coverage")
        plt.ylabel("Maximum Conductance")
        plt.legend()


if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv)
    seeders = option_import.select_seeders()

    directory = os.getcwd()

    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/conductance_{date}"

    conductance_manager = ConductancePlotManager(seeders, save_name)

    reader = option_import.generate_reader()
    if reader is not None:
        conductance_manager.plot_with_lfr(reader)
    else:
        graph, _ = option_import.import_real(directory)
        print("Graph and community imported")
        save_name = f"{directory}/conductance_{date}_real.png"
        conductance_manager.plot_multicoverage(graph, save_name)

import matplotlib.pyplot as plt
import time

from module.import_options import Options
from module.seeding.seeder.spreadhub import Spreadhub
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
        cplot = ConductancePlot(graph)
        for label, seeds in seed_dict.items():
            print(label, len(seeds))
            start = time.time()
            cplot.plot_coverage(seeds, label)
            end = time.time()
            expand_time = self.stopWatch(end - start)
            print(f"{label}  Seed time = {expand_time}")


        start = time.time()
        cplot.plot_coverage_mfc()
        end = time.time()
        self.stopWatch(end - start)
        expand_time = self.stopWatch(end - start)
        print(f"mfc-original  Total time = {expand_time}")

        start = time.time()
        spread = Spreadhub(int(0.15 * len(graph.nodes)))
        cplot.plot_coverage(spread.seed(graph), "Spreadhub")
        end = time.time()
        self.stopWatch(end - start)

        expand_time = self.stopWatch(end - start)
        print(f"Spreadhub  Total time = {expand_time}")

        self._plot_lables()

    #TODO remove
    @staticmethod
    def stopWatch(value):
        #'https://stackoverflow.com/questions/5890304/stopwatch-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa'
        '''From seconds to Days;Hours:Minutes;Seconds'''

        valueD = (((value / 365) / 24) / 60)
        Days = int(valueD)

        valueH = (valueD - Days) * 365
        Hours = int(valueH)

        valueM = (valueH - Hours) * 24
        Minutes = int(valueM)

        valueS = (valueM - Minutes) * 60
        Seconds = int(valueS)

        times = f"Days {Days}, Hours {Hours}, Minutes {Minutes}, Seconds {Seconds}"
        print(times)
        return times



    def plot_multicoverage(self, graph, save_name):
        seed_dict = {}

        for seeder in self.seeders:
            print("Processing", seeder.name)
            start = time.time()
            seeds = seeder.seed(graph)
            end = time.time()
            seed_time = self.stopWatch(end - start)
            print(f"{seeder.name}  Seed time = {seed_time}")


            seed_dict[seeder.name] = seeds

        print("Plotting tools...")
        self.plot_coverages(graph, seed_dict)
        if save_name != '':
            plt.savefig(save_name)
        #plt.show()
        plt.close()

    def plot_with_lfr(self, reader, label='LFR'):
        lfr_dict = reader.read()
        for key, value in lfr_dict.items():
            print(key)
            if len(key) is 2:
                size, mix = key
                overlap = None
            else:
                size, mix, overlap = key
            graph, _ = value
            save_loc = f"{self.save_base}_%s_%s_%s_%s.png" % (label, size, mix, overlap)
            plt.title(f"Size: {size} Mix: {mix} Overlap {overlap}")
            self.plot_multicoverage(graph=graph, save_name=save_loc)

    @staticmethod
    def _plot_lables():
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

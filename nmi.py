from tqdm import tqdm

from module.lfr.nmi_plot import PlotNMI
from module.lfr.lfr_reader import LFRReader
from module.lfr.community_writer import WriteCommunities
from module.expansion.ppr import PPR
from module.import_options import Options
from module.seeding.seeder.spreadhub import Spreadhub


class NMIManager:

    def __init__(self, cd_seeders):
        self.cd_seeders = cd_seeders

    def plot(self, reader, location=''):
        lfr = WriteCommunities(reader)

        seeders.append(Spreadhub(int(float(reader.network_sizes[0]) * 0.2)))

        for seeder in seeders:
            lfr.calculate_communities(reader, seeder)
        lfr.calculate_mfc(reader)

        plot_tuples = []
        for seeder in tqdm(seeders):
            method_tup = (seeder.name, seeder.threshold)
            plot_tuples.append(method_tup)
        plot_tuples.append(("mfc-original", 0))

        lfr_plot = PlotNMI(plot_tuples, save_loc=location)
        lfr_plot.plot(reader.network_sizes, reader.mixing_parameters, reader.overlapping_fractions)

    def read_real(self, network, truth):
        reader = LFRReader([1000], [0.1], [0.1])
        writer = WriteCommunities(reader)
        communities = {}

        for seeder in self.cd_seeders:
            print(seeder)
            key = ('', '', '')
            communities[key] = []

            ppr = PPR()
            seeds = seeder.seed(network)

            for seed in seeds:
                seeds = set(network[seed])
                seeds.add(seed)
                bestset = ppr.ppr_rank(network, seed)
                communities[key].append(bestset)

            method = f'custom{len(network)}_{seeder.name}'
            writer.save(truth, communities, key, '', method)
            lfr_plot = PlotNMI((), save_loc='')
            nmi = lfr_plot.read(method, '', '', '', '')
            print(f"{seeder.name}   NMI: {nmi}")


if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv, parameters="smoc")
    seeders = option_import.select_seeders()

    directory = os.getcwd()

    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}"

    nmi_manager = NMIManager(seeders)

    reader = option_import.generate_reader()
    if reader is not None:
        nmi_manager.plot(reader, save_name)
    else:
        graph, communities = option_import.import_real(directory, need_truth=True)
        print("Graph and community imported")
        seeders.append(Spreadhub(int(float(len(graph)) * 0.2)))
        nmi_manager.read_real(graph, communities)

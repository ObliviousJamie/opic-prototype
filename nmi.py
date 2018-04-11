from module.LFR.plotLFR import PlotLFR
from module.LFR.readLFR import ReadLFR
from module.LFR.writeLFR import WriteLFR
from module.expansion.PPR import PPR
from module.import_options import Options
from module.seeding.spreadhub_seed import Spreadhub


class NMIManager:

    def plot(self, seeders, reader, added_loc=''):
        lfr = WriteLFR(reader)

        seeders.append(Spreadhub(int(float(reader.network_sizes[0]) * 0.2)))

        for seeder in seeders:
            lfr.calculate_communities(reader, seeder)
        lfr.calculate_mfc(reader)

        plot_tuples = []
        for seeder in seeders:
            method_tup = (seeder.name, seeder.threshold)
            plot_tuples.append(method_tup)
        plot_tuples.append(("mfc-original", 0))

        save = (f"/home/jmoreland/Pictures/PRJ{added_loc}")
        lfr_plot = PlotLFR(plot_tuples, save_loc=save)
        lfr_plot.plot(reader.network_sizes, reader.mixing_parameters, reader.overlapping_fractions)

    def read_real(self, graph_seeders, graph, truth):
        reader = ReadLFR([1000],[0.1],[0.1])
        writer = WriteLFR(reader)
        communities = {}

        for seeder in graph_seeders:
            print(seeder)
            key = ('','','')
            communities[key] = []

            ppr = PPR(graph)
            seeds = seeder.seed(graph)

            for seed in seeds:
                seed = graph[seed]
                bestset = ppr.PPRRank(graph, 0.99, 0.0001, seed)
                communities[key].append(bestset)

            method = f'custom{len(graph)}_{seeder.name}'
            writer.save(truth, communities, key, '', method)
            lfr_plot = PlotLFR((), save_loc='')
            nmi = lfr_plot.read(method, '', '', '', '')
            print(f"{seeder.name}   NMI: {nmi}")


if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv)
    seeders = option_import.select_seeders()

    directory = os.getcwd()

    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/nmi_{date}"

    nmi_manager = NMIManager()

    reader = option_import.generate_reader()
    if reader is not None:
        nmi_manager.plot(seeders, reader, '/all')
    else:
        print(seeders)
        graph, truth = option_import.import_real(directory, need_truth=True)
        print("Graph and community imported")
        nmi_manager.read_real(seeders, graph, truth)

#standard = samples.standard()
#
#reader = ReadLFR([1000], [0.1], overlapping_fractions=[0.1, 0.3, 0.5])
#plot(standard, reader, '/all_nmi')

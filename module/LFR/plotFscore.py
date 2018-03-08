from module.graph.tools.expand_seeds import SeedExpansion
from module.statistics.fscore import FScore
import matplotlib.pyplot as plt
import csv


class PlotFscore:

    def __init__(self, seeders):
        self.seeders = seeders

    def plot(self, seeder_list, fscore_calc):
        for seeder in seeder_list:
            seeds = seeder.seed()

    def fscores(self, real, found):
        fscore = FScore(real, found)
        f1 = fscore.f1()
        f2 = fscore.f2()
        return f1, f2

    def lfr_fscores(self, reader, save_location=''):
        rows = {}

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

            for seeder in self.seeders:
                generated = f"{size}-{mix}-{overlap} {seeder.name}"

                print(f"Seeding {seeder.name}")
                seeds = seeder.seed(graph)
                found = expander.expand(seeds, graph)
                f1, f2 = self.fscores(real_communities, found)
                rows[f"f1 {generated}"] = f1
                rows[f"f2 {generated}"] = f2

        if save_location != '':
            self.write(rows, save_location)

    def write(self, rows_dict, save_location):
        print('Writing...')
        fieldnames = sorted(list(rows_dict.keys()))
        with open(save_location, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= fieldnames)
            writer.writeheader()
            writer.writerow(rows_dict)
        print('Done')








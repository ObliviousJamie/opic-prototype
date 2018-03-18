from module.graph.tools.expand_seeds import SeedExpansion
from module.graph.tools.write_csv import WriteCSV
from module.statistics.fscore import FScore


class FscoreCalculator:

    def __init__(self, seeders, save_location):
        self.seeders = seeders
        self.expander = SeedExpansion()
        self.save_location = save_location

    def fscores(self, real, found):
        fscore = FScore(real, found)
        f1 = fscore.f1()
        f2 = fscore.f2()
        return f1, f2

    def lfr_fscores(self, reader):
        rows = {}

        lfr_dict = reader.read()
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
                found = self.expander.expand(seeds, graph)
                f1, f2 = self.fscores(real_communities, found)
                rows[f"f1 {generated}"] = f1
                rows[f"f2 {generated}"] = f2

        if self.save_location != '':
            WriteCSV.write(rows_dict=rows, save_location=self.save_location)

        return rows

    def imported_fscores(self, graph, communities, label):
        rows = {}
        for seeder in self.seeders:
            header_label = f"{label} {seeder.name}"
            print(f"Seeding {seeder.name}...")
            seeds = seeder.seed(graph)
            print(f"Expanding seeds...")
            found = self.expander.expand(seeds, graph)
            print(f"Computing fscores...")
            f1, f2 = self.fscores(communities, found)
            rows[f"f1 {header_label}"] = f1
            rows[f"f2 {header_label}"] = f2

        if self.save_location != '':
            WriteCSV.write(rows_dict=rows, save_location=self.save_location)

        return rows










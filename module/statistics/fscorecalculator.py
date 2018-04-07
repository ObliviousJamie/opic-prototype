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
        avg_seed = {}
        total_seeds = {}

        lfr_dict = reader.read()
        for key, value in lfr_dict.items():

            if len(key) is 2:
                size, mix = key
                overlap = ''
            else:
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

                avg_seed.setdefault(seeder.name, []).append((f1,f2))
                total_seeds.setdefault(seeder.name, 0)
                total_seeds[seeder.name] += len(seeds)

                rows[f"f1 {generated}"] = f1
                rows[f"f2 {generated}"] = f2

        if self.save_location != '':
            WriteCSV.write(rows_dict=rows, save_location=self.save_location)

        for method, size in sorted(total_seeds.items()):
            print(f"{method} has {size} seeds")

        self.temp(avg_seed)

        return rows

    def temp(self, avg_seed):
        best_f1 = (0, "")
        best_f2 = (0, "")
        averages = {}

        for seeder_name, fscore_list in avg_seed.items():
            total_f1 = 0
            total_f2 = 0

            for fpair in fscore_list:
                f1, f2 = fpair
                total_f1 += f1
                total_f2 += f2

            avg_f1 = total_f1 / len(fscore_list)
            avg_f2 = total_f2 / len(fscore_list)

            averages[seeder_name] = (avg_f1, avg_f2)

            if avg_f1 > best_f1[0]:
                best_f1 = (avg_f1, seeder_name)
            if avg_f2 > best_f2[0]:
                best_f2 = (avg_f2, seeder_name)

        print(avg_seed)

        print()
        print()
        print()
        score, name = best_f1
        print(f"Best f1 {name} with average of {score}")
        score, name = best_f2
        print(f"Best f2 {name} with average of {score}")

        print()
        print()
        print()

        for key, value in sorted(averages.items()):
            f1, f2 = value
            print(f"{key} with accuracy of F1: {f1}     F2: {f2}")


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










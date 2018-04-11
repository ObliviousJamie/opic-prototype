from module.lfr.helper import LFRHelper
from module.crawling.mfc import MFC
from module.statistics.fscore.fscore import FScore
from module.tools.extra.expand_seeds import SeedExpansion
from module.tools.extra.write_csv import WriteCSV


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
        total_seeds = {}

        lfr_dict = reader.read()
        networks = ["Technique"]
        all_scores = {}

        for key, value in lfr_dict.items():
            size, mix, overlap = LFRHelper.extract_key(key)

            graph, communities = value

            real_communities = {}
            for vertex, community in communities.items():
                for single_community in community:
                    real_communities.setdefault(single_community, [])
                    real_communities[single_community].append(vertex)

            networks.append(f"{size}-{mix}-{overlap}")

            for seeder in self.seeders:
                print(f"Seeding {seeder.name}")
                seeds = seeder.seed(graph)
                found = self.expander.expand(seeds, graph)
                f1, f2 = self.fscores(real_communities, found)

                total_seeds.setdefault(seeder.name, 0)
                total_seeds[seeder.name] += len(seeds)

                all_scores.setdefault(seeder.name, []).append((f1, f2))

            mfc = MFC(graph, '1')
            f1, f2 = self.fscores(real_communities, mfc.communities())
            all_scores.setdefault('mfc-orignal', []).append((f1, f2))

        if self.save_location != '':
            WriteCSV.write_scores(networks, all_scores, self.save_location)
            WriteCSV.write_scores(networks, all_scores, self.save_location, beta=2)

        return all_scores

    def imported_fscores(self, graph, communities, label):
        all_scores = {}

        print("Calculating mfc-original")
        mfc = MFC(graph, '1')
        f1, f2 = self.fscores(communities, mfc.communities())
        all_scores.setdefault('mfc-orignal', []).append((f1, f2))

        for seeder in self.seeders:
            print(f"Seeding {seeder.name}...")
            seeds = seeder.seed(graph)
            print(f"Expanding seeds...")
            found = self.expander.expand(seeds, graph)
            print(f"Computing fscores...")
            f1, f2 = self.fscores(communities, found)
            all_scores.setdefault(seeder.name, []).append((f1, f2))

        if self.save_location != '':
            network = ["Custom network"]
            WriteCSV.write_scores(network, all_scores, self.save_location)
            WriteCSV.write_scores(network, all_scores, self.save_location, beta=2)

        return all_scores

import copy

import matplotlib.pyplot as plt
from random import choice

from module.tools.extra.expand_seeds import SeedExpansion
from module.statistics.fscore import FScore


class SeedPlot:

    def __init__(self, reader, save_location=None):
        self.lfr_dict = reader.read()
        self.expander = SeedExpansion()
        self.save_location = save_location

    def plot_nmi(self):
        for key, value in self.lfr_dict.items():
            if len(key) is 2:
                size, mix = key
                overlap = ''
            else:
                size, mix, overlap = key

            graph, _ = value

            seed_dict = self._pick_seeds(graph)

    def plot_fscore(self, beta, seeders=None):
        for key, value in self.lfr_dict.items():
            graph, communities = value
            real_communities = {}
            for vertex, community in communities.items():
                for single_community in community:
                    real_communities.setdefault(single_community, [])
                    real_communities[single_community].append(vertex)

            seed_dict = {}

            if seeders is None:
                seed_dict = self._pick_seeds(graph)
            else:
                for seeder in seeders:
                    seeds = seeder.seed(graph)
                    seed_dict[len(seeds)] = seeds

            for total, seeds in seed_dict.items():
                found = self.expander.expand(seeds, graph)
                fscore = FScore(real_communities, found)
                score = fscore.fscore(beta)

                percentage = int(total / len(graph.nodes) * 100)
                print(percentage)
                plt.plot(percentage, score, 'ro')
                print(f"Total {score}   Seeds {len(seeds)}")

            self._add_labels(f"F{beta} score")
            plt.show()

            if self.save_location:
                unique_str = str(key).replace('[', '')
                plt.savefig(f"{self.save_location}/{unique_str}.png")
            else:
                plt.show()

    def _pick_seeds(self, graph):
        total_size = len(graph.nodes)
        all_seeds = {}
        node_list = list(graph.nodes)

        ten_percent = int(total_size * (1 / 20))
        for i in range(1, 21):
            total_seeds = ten_percent * i
            all_seeds.setdefault(total_seeds, set())

            if i is not 1:
                all_seeds[total_seeds] = copy.deepcopy(all_seeds[ten_percent * (i - 1)])

            for j in range(0, int(ten_percent)):
                random_seed = choice(node_list)
                all_seeds[total_seeds].add(random_seed)

                node_list.remove(random_seed)

        return all_seeds

    def _add_labels(self, metric):
        plt.title(f"Seeds against {metric}")
        plt.xlabel("Percentage of tools used as seeds")
        plt.ylabel(metric)
        plt.axis((0, 100, 0, 1.0))
        # plt.legend()

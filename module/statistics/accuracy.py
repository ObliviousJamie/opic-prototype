import numpy

from module.graph.tools.expand_seeds import SeedExpansion


class Stats:

    def __init__(self, true_communities):
        self.true_communities = true_communities
        self.size = 0
        for community in true_communities.values():
            self.size += len(community)

    def compare(self, found_communities):
        acc_array = []
        found = []
        for seed in found_communities.keys():
            for key, community in self.true_communities.items():
                if seed in community:
                    print("Seed %s" % seed)
                    acc_array.append(self.accuracy(found_communities[seed], community, key))
                    if key not in found:
                        found.append(key)

        print("Found %s/42" % len(found))
        print(sorted(found))
        print(sorted(self.true_communities.keys()))
        setf = set(found)
        sett = set(self.true_communities.keys())
        set1 = list(sett - setf)
        print(set1)
        return numpy.mean(acc_array)

    def accuracy(self, found_set, real_set, real_community):
        tp = 0
        fn = 0
        for vertex in real_set:
            if vertex in found_set:
                tp += 1
            else:
                fn += 1

        fp = 0
        for v in found_set:
            if v not in real_set:
                fp += 1

        negatives = self.size - len(real_set)
        tn = negatives - (fn + fp)
        acc = ((tp + tn) / (tp + fp + tn + fn)) * 100

        print("Community: %s , TP %s, FN %s, FP %s, Real size %s , Found size %s" % (
            real_community, tp, fn, fp, len(real_set), len(found_set)))
        print("Accuracy %s" % acc)
        # print(found_set)
        print()
        return acc

    @staticmethod
    def print_expanded(seeder, graph):
        seeds = seeder.seed(graph)
        expander = SeedExpansion()

        discovered_communities = expander.expand(seeds, graph, tol=0.01, use_neighborhood=True)
        for key, value in discovered_communities.items():
            print("Seed: %s found:  %s" % (key, value))
import numpy


class Accuracy:

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
                    accuracy = self.accuracy(found_communities[seed], community, key)

                    print(f"Seed:{seed} Accuracy:{accuracy}")

                    acc_array.append(accuracy)
                    if key not in found:
                        found.append(key)

        average = numpy.mean(acc_array)

        print(f"Average accuracy: {average}")

        return average

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
        print()
        return acc

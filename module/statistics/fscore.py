import statistics


class FScore:

    def __init__(self, real, discovered):
        self.real = real
        self.discovered = discovered

    def f1(self):
        return self.fscore(beta=1)

    def f2(self):
        return self.fscore(beta=2)

    def fscore(self, beta):
        scores = []
        for _, community in self.real.items():
            max_score = 0
            for _, found_community in self.discovered.items():
                precision, recall = self.precision_recall(community, found_community)
                score = 0
                if precision > 0 and recall > 0:
                    score = self.calculate(precision, recall, beta)
                if score > max_score:
                    max_score = score
            scores.append(max_score)

        avg = sum(scores) / len(scores)
        return avg

    def calculate(self, precision, recall, beta):
        beta_square = beta * beta
        denominator = (beta_square * precision) + recall
        f = (1 + beta_square) * (precision * recall) / denominator
        return f

    def precision_recall(self, real_community, found_community):
        found_set = set(found_community)
        real_set = set(real_community)

        tp = real_set.intersection(found_set)

        precision = len(tp) / len(found_set)
        recall = len(tp) / len(real_set)

        return precision, recall

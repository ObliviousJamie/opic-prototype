class FScore:

    def __init__(self, real, discovered):
        self.real = real
        self.discovered = discovered

    def f1(self):
        return self.f_score(beta=1)

    def f2(self):
        return self.f_score(beta=2)

    def f_score(self, beta):
        real = self._compare_loop(beta, self.real, self.discovered)
        discovered = self._compare_loop(beta, self.discovered, self.real)
        avg = (real + discovered) / 2
        return avg

    def _compare_loop(self, beta, outer, inner):
        scores = []
        for _, community in outer.items():
            max_score = 0
            if len(community) >= 15:
                for _, found_community in inner.items():
                    precision, recall = self._precision_recall(community, found_community)
                    score = 0
                    if precision > 0 and recall > 0:
                        score = self._calculate(precision, recall, beta)
                    if score > max_score:
                        max_score = score
                scores.append(max_score)
        avg = 0
        if len(scores) > 0:
            avg = sum(scores) / len(scores)
        return avg

    @staticmethod
    def _calculate(precision, recall, beta):
        beta_square = beta * beta
        denominator = (beta_square * precision) + recall
        f = (1 + beta_square) * (precision * recall) / denominator
        return f

    @staticmethod
    def _precision_recall(real_community, found_community):
        found_set = set(found_community)
        real_set = set(real_community)

        tp = real_set.intersection(found_set)

        precision = len(tp) / len(found_set)
        recall = len(tp) / len(real_set)

        return precision, recall

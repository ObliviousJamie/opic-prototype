import collections


class PPR:
    """
    This work is not my own

    Credit to:
    Implementation based on: David Gleich (dgleich): https://gist.github.com/dgleich/6201856
    Overlapping Community Detection Using Neighborhood-Inflated Seed Expansion: https://arxiv.org/pdf/1503.07439.pdf
    """

    def __init__(self, alpha=0.99, tol=0.0001):
        self.alpha = alpha
        self.tol = tol

    def ppr_rank(self, graph, seed):
        sv = self._sorted_set(graph, seed)
        best_set = {sv[0][0]}
        best_array = self._min_cut(graph, best_set, sv)
        return best_array[0]

    def ppr_conductance(self, graph, seed):
        sv = self._sorted_set(graph, seed)
        best_set = sv[0]

        return self._min_cut(graph, best_set, sv)

    def _sorted_set(self, graph, seed):
        x = {}
        r = {}
        Q = collections.deque()
        for s in seed:
            r[s] = 1.0 / len(seed)
            Q.append(s)
        while len(Q) > 0:
            v = Q.popleft()

            if v not in x:
                x[v] = 0.

            x[v] += (1 - self.alpha) * r[v]

            mass = self.alpha * r[v] / (2 * len(graph[v]))

            for u in graph[v]:
                if u not in r:
                    r[u] = 0.

                if r[u] < len(graph[u]) * self.tol <= r[u] + mass:
                    Q.append(u)

                r[u] += mass

            r[v] = mass * len(graph[v])
            if r[v] >= len(graph[v]) * self.tol:
                Q.append(v)

        # Normalise by degree and find community
        for v in x:
            x[v] = x[v] / len(graph[v])

        # sort by keys
        sv = sorted(x.items(), key=lambda x: x[1], reverse=True)

        return sv

    @staticmethod
    def _min_cut(graph, best_set, sorted_set):
        graph_volume = (len(graph.edges) * 2)

        S = set()
        volume_set = 0.
        cut_set = 0.
        best_condition = 1.

        for p in sorted_set:
            s = p[0]
            volume_set += len(graph[s])
            for v in graph[s]:

                if v in S:
                    cut_set -= 1

                else:
                    cut_set += 1

            S.add(s)

            if cut_set / min(volume_set, graph_volume - volume_set) < best_condition:
                best_condition = cut_set / min(volume_set, graph_volume - volume_set)
                best_set = set(S)

        return [best_set, best_condition]

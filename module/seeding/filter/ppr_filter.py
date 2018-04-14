from module.expansion.ppr import PPR
from module.seeding.filter.neighborhood_filter import NeighborhoodFilter


class PPRFilter(NeighborhoodFilter):

    def __init__(self, tol):
        super().__init__()
        self.tol = tol
        self.name = 'ppr_filter'

    def filter(self, seeds, graph):
        ppr = PPR(tol=self.tol)
        visited = set()

        new_seeds = []

        for seed in seeds:
            if seed not in visited:
                new_seeds.append(seed)
                best_set = ppr.ppr_rank(graph, seed)
                for v in best_set:
                    visited.add(v)
        return new_seeds

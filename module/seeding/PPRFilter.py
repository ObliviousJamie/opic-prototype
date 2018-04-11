from module.expansion.ppr import PPR
from module.seeding.seed_filter import DefaultFilter


class PPRFilter(DefaultFilter):

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
                bestset = ppr.ppr_rank(graph, seed)
                for v in bestset:
                    visited.add(v)
        print("Was", len(seeds))
        print("Now", len(new_seeds))

        return new_seeds



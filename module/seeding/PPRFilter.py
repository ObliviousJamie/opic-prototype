from module.expansion.PPR import PPR
from module.seeding.seed_filter import DefaultFilter


class PPRFilter(DefaultFilter):

    def __init__(self, tol):
        super().__init__()
        self.tol = tol
        self.name = 'ppr_filter'

    def filter(self, seeds, graph):
        ppr = PPR(graph)
        visited = set()

        new_seeds = []

        for seed in seeds:
            if seed not in visited:
                new_seeds.append(seed)
                bestset = ppr.PPRRank(graph, 0.99, self.tol, [seed])
                for v in bestset:
                    visited.add(v)
        print("Was", len(seeds))
        print("Now", len(new_seeds))

        return new_seeds



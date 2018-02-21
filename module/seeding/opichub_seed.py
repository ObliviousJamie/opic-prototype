from module.OPIC import OPIC
from module.seeding.hub_seed import HubSeeder


class SeedOPICHub(HubSeeder):

    def __init__(self, seed_limit, start=None, return_type="integer"):
        super(SeedOPICHub, self).__init__(seed_limit=seed_limit, return_type=return_type)
        self.start = start

    def seed(self, G):
        start = self.start
        if start is None:
            start = self.random_vertex(G)

        opic = OPIC(G, 40)
        opic.visit(start)
        iterations = len(G.edges())

        seeds = []
        candidates = []
        for _ in range(iterations):
            max_vertex = max(opic.cash_current, key=lambda i: opic.cash_current[i])
            max_cash = opic.cash_current[max_vertex]
            pair = (max_cash, max_vertex)

            neighbor = self.neighbor(G, max_vertex, seeds)

            if neighbor is None:
                self.maintain_heap(seeds, pair)
            else:
                if self.is_candidate(neighbor, pair):
                    candidates.append(neighbor)
            opic.visit(max_vertex)

        print(sorted(seeds, reverse=True))
        seeds = self.filter_candidates(candidates, seeds, G)
        print(sorted(seeds))

        return seeds


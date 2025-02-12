from module.crawling.mfc import MFC
from module.seeding.seeder.alternative.hub_seed import HubSeeder


class SeedMinhubMFC(HubSeeder):

    def __init__(self, seed_limit, start=None, return_type="string"):
        super(SeedMinhubMFC, self).__init__(seed_limit=seed_limit, return_type=return_type)
        self.start = start

    def seed(self, graph):
        start = self.start
        if start is None:
            start = self.random_vertex(graph)

        mfc = MFC(graph, start)

        heap = []
        candidate_backlog = []

        while not mfc.empty():
            max_vertex = mfc.next()
            max_ref = mfc.max_references[-1]
            # Invert to make a max heap
            inverted_ref = max_ref * -1
            ref_pair = (inverted_ref, max_vertex)

            neighbor_tuple = self.neighbor(graph, max_vertex, heap)
            if neighbor_tuple is not None:
                if self.is_candidate(neighbor_tuple, ref_pair):
                    candidate_backlog.append(ref_pair)
            else:
                self.maintain_heap(heap, ref_pair)

        seeds = self.filter_candidates(candidate_backlog, heap, graph)

        return seeds

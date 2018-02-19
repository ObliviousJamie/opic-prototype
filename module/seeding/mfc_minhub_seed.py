import numpy as np
import heapq

from module.MFC import MFC
from module.seeding.threshold_seed import ThresholdSeeder


class SeedMinMFC(ThresholdSeeder):

    def __init__(self, threshold, seed_limit, start=None, return_type="integer"):
        super(SeedMinMFC, self).__init__(threshold=threshold, return_type=return_type)
        self.start = start
        self.seed_limit = seed_limit

    def seed(self, G):
        start = self.start
        if start is None:
            start = self.random_vertex(G)

        mfc = MFC(G, start)

        heap = []

        while not mfc.empty():
            max_vertex = mfc.next()
            max_ref = mfc.y[-1]
            # Invert to make a max heap
            inverted_ref = max_ref * -1
            ref_pair = (inverted_ref, max_vertex)

            neighbor_tuple = self.neighbor(G, max_vertex, heap)
            if neighbor_tuple is not None:
                self.resolve_neighborhood(neighbor_tuple, ref_pair, heap)
            else:
                self.maintain_heap(heap, ref_pair)

        print(sorted(heap))

        return heap

    def maintain_heap(self, heap, ref_tuple):
        if len(heap) < self.seed_limit:
            heapq.heappush(heap, ref_tuple)
        else:
            heapq.heappushpop(heap, ref_tuple)

    def resolve_neighborhood(self, heap_pair, ref_pair, heap):
        if ref_pair[0] > heap_pair[0]:
            heap[heap.index(heap_pair)] = ref_pair
            heapq.heapify(heap)
            print("Resolve", ref_pair, heap_pair)

    def neighbor(self, graph, vertex, heap):
        for ref, min_node in heap:
            if graph.has_edge(vertex, min_node):
                return (ref, min_node)
        return None

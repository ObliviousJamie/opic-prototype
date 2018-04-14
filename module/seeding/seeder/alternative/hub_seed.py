import heapq

from module.seeding.seeder.seeder import Seeder


class HubSeeder(Seeder):

    def __init__(self, seed_limit, start=None, return_type="string"):
        super(HubSeeder, self).__init__(return_type=return_type)
        self.start = start
        self.seed_limit = seed_limit

    def maintain_heap(self, heap, ref_tuple):
        if len(heap) < self.seed_limit:
            heapq.heappush(heap, ref_tuple)
        else:
            heapq.heappushpop(heap, ref_tuple)

    def resolve_neighborhood(self, heap_pair, ref_pair, heap):
        if ref_pair[0] > heap_pair[0]:
            heap[heap.index(heap_pair)] = ref_pair
            heapq.heapify(heap)

    def is_candidate(self, heap_pair, ref_pair):
        if ref_pair[0] > heap_pair[0]:
            return True
        return False

    def neighbor(self, graph, vertex, heap):
        for ref, node in heap:
            if graph.has_edge(vertex, node):
                return ref, node
        return None

    def filter_candidates(self, candidates, raw_heap, graph):
        n = self.seed_limit
        final_seeds = []
        visited = set()
        potential_seeds = candidates + raw_heap
        potential_seeds = sorted(potential_seeds, reverse=True)

        for _, seed in potential_seeds:
            if n > 0:
                if seed not in visited:
                    final_seeds.append(seed)
                    visited.add(seed)
                    visited = visited.union(list(graph[seed]))
                    n -= 1
            else:
                break

        return final_seeds

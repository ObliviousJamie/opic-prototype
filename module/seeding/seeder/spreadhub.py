from tqdm import tqdm

from module.seeding.seeder.seeder import Seeder


class Spreadhub(Seeder):

    def __init__(self, seed_limit, return_type='string'):
        super(Spreadhub, self).__init__(return_type=return_type)
        self.seed_limit = seed_limit
        self.name = 'Spreadhub'

    def seed(self, graph):
        degree_seq = sorted([(degree, vertex) for vertex, degree in graph.degree()], reverse=True)

        seeds = []
        visited = set()

        last_degree = -1
        for degree, vertex in tqdm(degree_seq, desc=f"{self.name} finding seeds"):
            if len(seeds) < self.seed_limit and vertex not in visited:
                seeds.append(vertex)
                visited.update(list(graph[vertex]))
            if len(seeds) >= self.seed_limit and vertex not in visited:
                if degree == last_degree:
                    seeds.append(vertex)
                    visited.update(list(graph[vertex]))
                else:
                    return seeds
            last_degree = degree

        print("Not enough seeds", len(seeds))

        return seeds

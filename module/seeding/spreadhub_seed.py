from module.seeding.seed import Seeder


class Spreadhub(Seeder):

    def __init__(self, seed_limit, return_type='string'):
        super(Spreadhub, self).__init__(return_type=return_type)
        self.seed_limit = seed_limit
        self.name = 'Spreadhub'

    def seed(self, G):
        degree_seq = sorted([(degree, vertex) for vertex, degree in G.degree()], reverse=True)

        print(degree_seq)

        seeds = []
        visited = set()

        last_degree = -1
        for degree, vertex in degree_seq:
            if len(seeds) < self.seed_limit and vertex not in visited:
                seeds.append(vertex)
                visited.update(list(G[vertex]))
            if len(seeds) >= self.seed_limit and vertex not in visited:
                if degree == last_degree:
                    seeds.append(vertex)
                    visited.update(list(G[vertex]))
                else:
                    return seeds
            last_degree = degree

        print("Not enough seeds", len(seeds))

        return seeds

class DefaultFilter():

    def __init__(self):
        self.name = 'neighborhood_filter'

    def filter(self, seeds, graph):
        visited = set()
        new_seeds = []
        for seed in seeds:
            if seed not in visited:
                new_seeds.append(seed)
                visited.add(seed)
                neighbors = graph.neighbors(seed)
                for u in neighbors:
                    visited.add(u)

        return new_seeds





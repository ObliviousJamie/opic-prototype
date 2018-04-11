class NeighborExpand:

    def __init__(self, graph):
        self.graph = graph

    def expand_seeds(self, seeds):
        expanded_seeds = {}
        for seed in seeds:
            neighbors = self.graph.neighbors(seed)
            expanded_seeds[seed] = list(neighbors)
            if seed not in expanded_seeds[seed]:
                expanded_seeds[seed].append(seed)
        return expanded_seeds

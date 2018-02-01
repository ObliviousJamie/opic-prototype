from module.PPR import PPR
import matplotlib.pyplot as plt


class Coverage:

    def __init__(self, graph, seeds):
        self.graph = graph
        self.seeds = seeds

    def find_conductance(self, tol=0.0001, use_neighborhood=True):
        ppr = PPR(self.graph)
        community = []
        for seed in self.seeds:
            seed_array = self.graph[seed] if use_neighborhood else [seed]
            best = ppr.PPR_conductance(self.graph,seed_array, alpha=0.99, tol=tol)
            community.append((best[1], best[0]))
        return community

    def plot_coverage(self, label):
        x, y = [], []
        visited = []

        discovered_communities = self.find_conductance()
        sorted_communities = sorted(discovered_communities)
        for community_tuple in sorted_communities:
            for vertex in community_tuple[1]:
                if vertex not in visited:
                    visited.append(vertex)
                    coverage = (len(visited) / len(self.graph)) * 100
                    conductance = community_tuple[0]

                    x.append(coverage)
                    y.append(conductance)

        plt.plot(x, y, label=label ,linewidth=2)

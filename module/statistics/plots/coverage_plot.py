from random import choice

import networkx as nx

from module.crawling.mfc import MFC
from module.expansion.ppr import PPR
import matplotlib.pyplot as plt


class ConductancePlot:

    def __init__(self, graph):
        self.graph = graph

    def find_conductance(self, seeds, tol=0.0001, use_neighborhood=True):
        ppr = PPR(tol=tol)
        community = []
        for seed in seeds:
            seed_array = self.graph[seed] if use_neighborhood else [seed]
            best = ppr.ppr_conductance(self.graph, seed_array)
            community.append((best[1], best[0]))
        return community

    def plot_coverage(self, seeds, label):
        x, y = [], []
        visited = []

        discovered_communities = self.find_conductance(seeds)
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

    def plot_coverage_mfc(self):
        start = choice(list(self.graph.nodes))

        conductances = []
        coverages = []

        mfc = MFC(self.graph, start)
        community_dict = mfc.communities(delta=0.5)
        conductance_array = []
        for _, community in community_dict.items():
            conductance = nx.algorithms.conductance(self.graph, community)
            conductance_array.append((conductance, community))

        sorted_communities = sorted(conductance_array)

        total_visited = 0

        for conductance, community in sorted_communities:
            for _ in community:
                conductances.append(conductance)
                total_visited += 1
                coverage = ( total_visited / len(self.graph.nodes)) * 100
                coverages.append(coverage)

        plt.plot(coverages, conductances, label="mfc_original", linewidth=2)


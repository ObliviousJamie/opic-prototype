from random import choice

import time

from module.PPR import PPR


class plotLFR:

    def __init__(self, LFR_reader, seeder):
        self.LFR_reader = LFR_reader
        self.seeder = seeder

    def compute_communities(self, threshold):
        lfr_graphs = self.LFR_reader.read()
        communities = {}

        for key, value in lfr_graphs.items():
            graph, membership = value

            start = choice(list(graph.nodes))

            start_time = time.time()

            seeds = self.seeder.seed(graph, start, threshold, return_type="string")
            seed_time = time.time() - start_time
            print("Time to compute seeds: %s" % (seed_time))

            start_time = time.time()

            ppr = PPR(graph)
            communities[key] = []
            for seed in seeds:
                seed = graph[seed]
                bestset = ppr.PPRRank(graph,0.99,0.001,seed)
                communities[key].append(bestset)

            ppr_time = time.time() - start_time
            print("Time to compute ppr: %s" % (ppr_time))






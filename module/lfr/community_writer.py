import os
from random import choice

from tqdm import tqdm

from module.crawling.mfc import MFC
from module.expansion.ppr import PPR


class WriteCommunities:

    def __init__(self, write_truth=True):
        self.dir = os.path.dirname(__file__)

        prefix = "../../data/lfr/communities/"
        location = os.path.join(self.dir, prefix)
        self.location = location

        self.write_truth = write_truth

    def save(self, truth, result, key, threshold=0, method=""):

        nodes, mix, overlap = key
        unique_key = "%s_%s_%s" % (nodes, mix, overlap)
        unique_result_key = "%s_t%s" % (method, threshold)

        result_f = "%s%s_%s_result.txt" % (self.location, unique_key, unique_result_key)

        print(f"Saving communities for benchmark network of Size {nodes}, Mix: {mix} Overlap: {overlap} ")

        with open(result_f, "w") as f:
            for community_set in result[key]:
                output = ' '.join(community_set)
                print(output, file=f)

        if self.write_truth:
            truth_f = "%s%s_truth.txt" % (self.location, unique_key)
            truth_reverse = {}

            for vertex, community_array in truth.items():
                for community in community_array:
                    truth_reverse.setdefault(community, list())
                    truth_reverse[community].append(vertex)
            with open(truth_f, "w") as f:
                for value in truth_reverse.values():
                    output = ' '.join(value)
                    print(output, file=f)

    def calculate_communities(self, reader, seeder):
        lfr_graphs = reader.read()
        communities = {}
        memberships = []

        for key, value in lfr_graphs.items():
            graph, membership = value
            memberships.append(membership)
            seeds = seeder.seed(graph)

            ppr = PPR()
            communities[key] = []
            for seed in tqdm(seeds, desc=f"{seeder.name} expanding seeds to communities", unit="seed"):
                seeds = set(graph[seed])
                seeds.add(seed)
                best_set = ppr.ppr_rank(graph, seeds)
                communities[key].append(best_set)

            self.save(truth=membership, result=communities, key=key, threshold=seeder.threshold, method=seeder.name)

        return communities, memberships

    def calculate_mfc(self, reader):
        lfr_graphs = reader.read()
        communities = {}
        memberships = []

        for key, value in lfr_graphs.items():
            graph, membership = value
            memberships.append(membership)
            random = choice(list(graph.nodes))
            mfc = MFC(graph, random)

            communities[key] = []

            mfc_communities = mfc.communities()
            for index, items in mfc_communities.items():
                communities[key].append(items)

            self.save(truth=membership, result=communities, key=key, threshold=0, method='mfc-original')

        return communities, memberships

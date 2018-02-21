import os

from module.expansion.PPR import PPR


class WriteLFR:

    def __init__(self, LFR_reader, seeder, write_truth=True):
        self.LFR_reader = LFR_reader
        self.seeder = seeder

        prefix = "../../data/lfr/communities/"
        location = os.path.join(LFR_reader.dir, prefix)
        self.location = location

        self.write_truth = write_truth

    def save(self, truth, result, key, threshold=0, method=""):

        nodes, mix, overlap = key
        unique_key = "%s_%s_%s" % (nodes, mix, overlap)
        unique_result_key = "%s_t%s" % (method, threshold)

        result_f = "%s%s_%s_result.txt" % (self.location, unique_key, unique_result_key)

        print("Seeds: %s Key: %s Method: %s" % (len(result[key]), key, method))

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

    def calculate_communities(self, seeder):
        lfr_graphs = self.LFR_reader.read()
        communities = {}
        memberships = []

        for key, value in lfr_graphs.items():
            graph, membership = value
            memberships.append(membership)

            print("%s Seeding..." % seeder.name)
            seeds = seeder.seed(graph)

            ppr = PPR(graph)
            communities[key] = []
            for seed in seeds:
                seed = graph[seed]
                bestset = ppr.PPRRank(graph, 0.99, 0.001, seed)
                communities[key].append(bestset)

            self.save(truth=membership, result=communities, key=key, threshold=seeder.threshold, method=seeder.name)

        return communities, memberships


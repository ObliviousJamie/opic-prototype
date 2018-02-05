from module.PPR import PPR


class writeLFR:

    def __init__(self, LFR_reader, seeder):
        self.LFR_reader = LFR_reader
        self.seeder = seeder

    def save(self, truth, result):
        truth_reverse = {}

        for vertex, community_array in truth.items():
            for community in community_array:
                truth_reverse.setdefault(community, list())
                truth_reverse[community].append(vertex)

        print(len(truth_reverse))
        print(len(result.keys()))
        print(result)
        print(truth)
        print(truth_reverse)

        exit()

        # TODO Write out both truth and result into separate files called <vertex_no>_<tau>_<overlap>_<truth || result>

        with open("test.txt", "w") as f:
            for key in result.keys():
                output = result[key].join(" ")
                f.write(output)

        with open("test2.txt", "w") as f:
            for key in truth_reverse.keys():
                output = result[key].join(" ")
                f.write(output)

    def calculate_communities(self, threshold, start='1', method='mfcrank', write=True):
        lfr_graphs = self.LFR_reader.read()
        communities = {}
        memberships = []
        start = start

        for key, value in lfr_graphs.items():
            graph, membership = value
            memberships.append(membership)

            seeds = self.decide_seed(graph, start, threshold, method)

            ppr = PPR(graph)
            communities[key] = []
            for seed in seeds:
                seed = graph[seed]
                bestset = ppr.PPRRank(graph, 0.99, 0.001, seed)
                communities[key].append(bestset)

            self.save(truth=membership, result=communities)

        return communities, memberships

    # TODO refactor
    def decide_seed(self, graph, start, threshold, method):
        seeds = []
        if method == 'opic':
            seeds = self.seeder.seed(graph, start, threshold, return_type="string")
        elif method == 'mfcrank':
            seeds = self.seeder.seed_MFC_rank(graph, start, threshold, return_type="string")
        elif method == 'mfcseed':
            seeds = self.seeder.seed_MFC_rank(graph, start, threshold, return_type="string")
        return seeds

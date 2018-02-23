from module.expansion.PPR import PPR


class SeedExpansion:

    @staticmethod
    def expand(seeds, G, tol=0.0001, use_neighborhood=True):
        ppr = PPR(G)

        community = {}
        for seed in seeds:
            seed_array = G[seed] if use_neighborhood else [seed]
            best = ppr.PPRRank(G, 0.99, tol, seed_array)
            community[seed] = best

        return community

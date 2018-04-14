from tqdm import tqdm

from module.expansion.ppr import PPR


class SeedExpansion:

    @staticmethod
    def expand(seeds, G, tol=0.0001, use_neighborhood=True):
        ppr = PPR(tol=tol)

        community = {}
        for seed in tqdm(seeds, desc="Expanding seeds to communities", unit="seed"):

            if use_neighborhood:
                seed_array = set(G[seed])
            else:
                seed_array = set()

            seed_array.add(seed)

            best = ppr.ppr_rank(G, seed_array)
            community[seed] = best

        return community

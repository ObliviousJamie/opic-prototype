import collections


class PPR:
    """
    Implementation based on: David Gleich (dgleich): https://gist.github.com/dgleich/6201856
    Overlapping Community Detection Using Neighborhood-Inflated Seed Expansion: https://arxiv.org/pdf/1503.07439.pdf
    """
    def __init__(self, g):
        self.G = g

    def PPRRank(self, G, alpha, tol, seed):
        Gvol = (len(G.edges) * 2)

        x = {}  # Store x, r as dictionaries
        r = {}  # initialize residual
        Q = collections.deque()  # initialize queue
        for s in seed:
            r[s] = 1.0 / len(seed)
            Q.append(s)
        while len(Q) > 0:
            v = Q.popleft()  # v has r[v] > tol*deg(v)

            if v not in x:
                x[v] = 0.

            x[v] += (1 - alpha) * r[v]

            mass = alpha * r[v] / (2 * len(G[v]))

            for u in G[v]:  # for neighbors of u
                if u not in r:
                    r[u] = 0.

                if r[u] < len(G[u]) * tol <= r[u] + mass:
                    Q.append(u)  # add u to queue if large

                r[u] += mass

            r[v] = mass * len(G[v])
            if r[v] >= len(G[v]) * tol:
                Q.append(v)

        # Find cluster, first normalize by degree
        for v in x:
            x[v] = x[v] / len(G[v])

        # now sort x's keys by value, decreasing
        sv = sorted(x.items(), key=lambda x: x[1], reverse=True)

        S = set()
        volS = 0.
        cutS = 0.
        bestcond = 1.
        bestset = sv[0]

        for p in sv:
            s = p[0]  # get the vertex
            volS += len(G[s])  # add degree to volume
            for v in G[s]:

                if v in S:
                    cutS -= 1

                else:
                    cutS += 1

            S.add(s)

            if cutS / min(volS, Gvol - volS) < bestcond:
                bestcond = cutS / min(volS, Gvol - volS)
                bestset = set(S)  # make a copy

        return bestset

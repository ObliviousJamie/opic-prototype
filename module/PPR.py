import collections


class PPR:
    def __init__(self, g):
        self.G = g

    def rank(self, alpha, tol, seeds):
        x = {}  # Store x, r as dictionaries
        r = {}  # initialize residual
        Q = collections.deque()  # initialize queue
        for s in seeds:
            r[s] = 1.0 / len(seeds)
            Q.append(s)
        while len(Q) > 0.:
            v = Q.popleft()  # v has r[v] > tol*deg(v)
            degree_v = len(self.G[v])

            if v not in x:
                x[v] = 0.

            x[v] += (1 - alpha) * r[v]

            mass = alpha * r[v] / (2 * degree_v)

            for u in self.G[v]:  # for neighbors of u
                degree_u = len(self.G[u])
                if u not in r:
                    r[u] = 0.

                if r[u] < degree_u * tol <= r[u] + mass:
                    Q.append(u)  # add u to queue if large

                r[u] += mass

            r[v] = mass * degree_v
            if r[v] >= degree_v * tol:
                Q.append(v)

            for key, value in x.items():
                print('Key: %s   Value: %s' % (key, value))

            # Find cluster, first normalize by degree
            for v in x:
                x[v] = x[v] / degree_v

            # now sort x's keys by value, decreasing
            return sorted(x.items(), key=lambda x: x[1], reverse=True)

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

        #for key, value in x.items():
        #    print('Key: %s   Value: %s' % (key, value))
        #print(len(x.items()))

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

            #print("v: %s  cut: %4f  vol: %4f" % (s, cutS, volS))
            S.add(s)
            #print(S)

            if cutS / min(volS, Gvol - volS) < bestcond:
                bestcond = cutS / min(volS, Gvol - volS)
                bestset = set(S)  # make a copy

        #print("Best set conductance: %f" % (bestcond))
        #print("  set = ", str(bestset))
        return bestset

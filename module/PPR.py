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

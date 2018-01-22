import matplotlib.pyplot as plt
import matplotlib.colors as color
import networkx as nx
import random
import matplotlib.cm as cmx

from module.OPIC import OPIC
from module.PPR import PPR

G = nx.karate_club_graph()

# Virtual page
G.add_node(100)
for v in G:
    G.add_edge(100, v)

vertices_num = len(G)

start_vertex = random.choice(list(G.nodes))
print('%s' % start_vertex)

opic = OPIC(G, 120.0)

opic.visit(start_vertex)

for _ in range(34 * 300):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    opic.visit(max_val)

# print("cash")
# for key, value in sorted(opic.cash_current.items()):
#    print('%d   Rank: %f' % (key + 1, value))

print("history")
for key, value in sorted(opic.cash_history.items()):
    print('%d   Rank: %f' % (key + 1, value))

G.remove_node(100)

# pr = nx.pagerank(G,0.85)
# print("PageRank")
# for key, value in sorted(pr.items()):
#    print('%d   Rank: %f' % (key + 1, value))

vector = {}
for _ in range(2):
    opic.cash_history[100] = 0
    max_val = max(opic.cash_history, key=lambda i: opic.cash_history[i])
    vector[max_val] = 2

    for v in G[max_val]:
        vector[v] = 2
        opic.cash_history[max_val] = 0

    opic.cash_history[max_val] = 0

for key, value in vector.items():
    print('Key: %d   value: %d' % (key, value))

pr = nx.pagerank(G, 0.5, vector)
print("PPR")
for key, value in sorted(pr.items()):
    print('%d   Rank: %f' % (key + 1, value))

nx.draw(G, with_labels=True)
plt.show()

import collections

# setup the graph
G = {
    1: {2, 3, 5, 6},
    2: {1, 4},
    3: {1, 6, 7},
    4: ([2, 5, 7, 8, ]),
    5: ([1, 4, 6, 8, 9, 10, ]),
    6: ([1, 3, 5, 7, ]),
    7: ([3, 4, 6, 9, ]),
    8: ([4, 5, 9, ]),
    9: ([5, 7, 8, 20, ]),
    10: ([5, 11, 12, 14, 15, ]),
    11: ([10, 12, 13, 14, ]),
    12: ([10, 11, 13, 14, 15, ]),
    13: ([11, 12, 15, ]),
    14: ([10, 11, 12, 25, ]),
    15: ([10, 12, 13, ]),
    16: ([17, 19, 20, 21, 22, ]),
    17: ([16, 18, 19, 20, ]),
    18: ([17, 20, 21, 22, ]),
    19: ([16, 17, ]),
    20: ([9, 16, 17, 18, ]),
    21: ([16, 18, ]),
    22: ([16, 18, 23, ]),
    23: ([22, 24, 25, 26, 27, ]),
    24: ([23, 25, 26, 27, ]),
    25: ([14, 23, 24, 26, 27, ]),
    26: ([23, 24, 25, ]),
    27: ([23, 24, 25, ]),
}
Gvol = 102

G = nx.Graph(G)

# G is graph as dictionary-of-sets
alpha = 0.99
tol = 0.01
seed = [16]

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

for key, value in x.items():
    print('Key: %s   Value: %s' % (key, value))

# Find cluster, first normalize by degree
for v in x:
    x[v] = x[v] / len(G[v])

# now sort x's keys by value, decreasing
sv = sorted(x.items(), key=lambda x: x[1], reverse=True)

# for entry in sv:
#    for key,value in entry:
#        print('Key: %s Value: %s' % (key,value))

# sv = PPR(G).rank(0.99,0.01,[1])

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

    print("v: %4i  cut: %4f  vol: %4f" % (s, cutS, volS))
    S.add(s)
    print(S)

    if cutS / min(volS, Gvol - volS) < bestcond:
        bestcond = cutS / min(volS, Gvol - volS)
        bestset = set(S)  # make a copy

print("Best set conductance: %f" % (bestcond))
print("  set = ", str(bestset))

nx.draw(G, with_labels=True)
plt.show()

#G.add_node(100)
#for v in G:
#    G.add_edge(100, v)

start_vertex = random.choice(list(G.nodes))
print('%s' % start_vertex)

opic = OPIC(G, 10.0)

opic.visit(start_vertex)

for _ in range(34 * 300):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    opic.visit(max_val)

# print("cash")
# for key, value in sorted(opic.cash_current.items()):
#    print('%d   Rank: %f' % (key + 1, value))
color_map = []
alpha_map = []
order = sorted(opic.cash_history.keys())
for v in order:
    cash = opic.cash_history[v] * 1000
    color_map.append(cash)



print("history")
hist = sorted(opic.cash_history.items(), key=lambda x: x[1], reverse=True)
high = sorted(opic.visit_time.items(), key=lambda x: x[1], reverse=True)
print(hist)
for entry in hist:
    print('Index: %d   Rank: %f' % (entry[0], entry[1]))
for entry in high:
    # print('Index: %d   Highest: %s' % (entry[0] , entry[1][-1]))
    print('Index: %d   Time: %s' % (entry[0], entry[1]))

#G.remove_node(100)

nx.draw(G, with_labels=True)
plt.show()

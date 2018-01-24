import matplotlib.pyplot as plt
import networkx as nx
import random

from module.OPIC import OPIC
from module.PPR import PPR
import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../data/edgelist/eu-core')
fh = open(filename, 'rb')
G = nx.read_edgelist(fh)
fh.close()
options = {
    'node_size': 10,
    'line_color': 'grey',
    'linewidths': 0,
    'width': 0.05,
}

#G = nx.karate_club_graph()

opic = OPIC(G, 10)
rank = nx.pagerank(G)
hist = sorted(rank.items(), key=lambda x: x[1], reverse=True)
#for entry in hist:
#    print(entry)

opic.visit('390')
#opic.visit(19)

y =  []
x = []
current_max = 0
i = 0
seeds = []
for _ in range(3000):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    y.append(opic.cash_current[max_val])
    x.append(opic.time)
    max_cash = opic.cash_current[max_val]
    if((opic.cash_current[max_val] > current_max - (max_cash * .08)) and opic.time > 1250):
        plt.text(opic.time, opic.cash_current[max_val], max_val)

        if(max_val not in seeds):
            seeds.append(max_val)

        i+= 1
    if(opic.cash_current[max_val] > current_max):
        current_max = opic.cash_current[max_val]

    opic.visit(max_val)

print(i)

#plt.plot(x, y, linewidth=2.0)
#print(y)
#plt.show()
#exit()

#print("history")
#c = 0
#hist = sorted(opic.cash_history.items(), key=lambda x: x[1], reverse=True)
#seeds = {}
#visited = []
#for entry in hist:
#    if entry[0] not in seeds:
#        seeds[c] = [entry[0]]
#        print("Index: %s  Value: %f" % (entry[0], entry[1]))
#        visited.append(entry[0])
#        for u in G[entry[0]]:
#            if u not in visited:
#                visited.append(u)
#        c += 1
#        if c >= 42:
#            break
#
#print("Seeds" + str(len(seeds)))
#print(seeds)
pos = nx.spring_layout(G)

ppr = PPR(G)

community = {}
index = 0
print(len(seeds))
for seed in seeds:
    best = ppr.PPRRank(G, 0.99, 0.0001, [seed])
    community[seed] = best
    color = 'C' + str(index % 8)
    nx.draw_networkx_nodes(G, pos, best, node_color= color, node_size= 10 )
    index+=1

print(community)
nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
nx.draw_networkx_edges(G, pos, width=0.05, color='grey')
plt.show()

exit()

# Ground truth

filename = os.path.join(dir, '../data/ground-truth/eu-core-snipped')
fh = open(filename, 'rb')
T = nx.read_edgelist(fh)
fh.close()

community = '36'

tp = 0
fn = 0
for v in T[community]:
    if v in best:
        tp += 1
        print(v)
    else:
        fn += 1
        print(v)

fp = 0
for v in best:
    if v not in T[community]:
        fp += 1

print("True positive (Correctly returned) : %s" % (tp))
print("False negative (Not returned but should have been) : %s" % (fn))
print("False positive (Returned but shouldn't have been) : %s" % (fp))
print("Real community size %s" % (len(T[community])))
print("Identifed community size %s" % (len(best)))

#nx.draw(G,**options)
plt.show()

G = nx.karate_club_graph()

vertices_num = len(G)

start_vertex = random.choice(list(G.nodes))
print('%s' % start_vertex)

opic = OPIC(G, 120.0)

opic.visit(start_vertex)

for _ in range(34 * 300):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    opic.visit(max_val)

print("history")
for key, value in sorted(opic.cash_history.items()):
    print('%d   Rank: %f' % (key + 1, value))

hist = sorted(opic.cash_history.items(), key=lambda x: x[1], reverse=True)
for entry in hist:
    print('Index: %d   Rank: %f' % (entry[0], entry[1]))

nx.draw(G, with_labels=True)
plt.show()

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

G = nx.Graph(G)

print("2")
ppr = PPR(G)
ppr.PPRRank(G, 0.99, 0.01, [16])

nx.draw(G, with_labels=True)
plt.show()

start_vertex = random.choice(list(G.nodes))
print('%s' % start_vertex)

opic = OPIC(G, 10.0)

opic.visit(start_vertex)

for _ in range(34 * 300):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    opic.visit(max_val)

print("history")
hist = sorted(opic.cash_history.items(), key=lambda x: x[1], reverse=True)
print(hist)
for entry in hist:
    print('Index: %d   Rank: %f' % (entry[0], entry[1]))

nx.draw(G, with_labels=True)
plt.show()

import matplotlib.pyplot as plt
import networkx as nx
import random
import operator

from module.OPIC import OPIC

G = nx.karate_club_graph()
vertices_num = len(G)
#print('%s' % vertices_num )

start_vertex = random.choice(list(G.nodes))
print('%s' % start_vertex )

opic = OPIC(G, 20.0)

opic.visit(start_vertex)

for _ in range(34 * 100):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    opic.visit(max_val)

print("cash")
for key, value in sorted(opic.cash_current.items()):
    print('%d   Rank: %f' % (key + 1, value))

print("history")
for key, value in sorted(opic.cash_history.items()):
    print('%d   Rank: %f' % (key + 1, value))

#print("Node Degree")
#for v in G:
#    print('%s %s' % (v, G.degree(v)))

nx.draw(G, with_labels=True)
plt.show()

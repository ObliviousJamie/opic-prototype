import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import peakutils
from module.OPIC import OPIC
from module.PPR import PPR
from module.importData import ImportData
from module.stats import Stats
from random import *

imports = ImportData()

G = imports.text_graph('../data/edgelist/eu-core')

options = {
    'node_size': 10,
    'line_color': 'grey',
    'linewidths': 0,
    'width': 0.05,
}

G = nx.karate_club_graph()
opic = OPIC(G, 10)
opic.visit(7)
#opic.visit('390')
#G.add_node('1005')
#for v in G:
#    G.add_edge('1005',v)

y = []
x = []
seeds = []
maximum = np.empty([1, 3000])
np_time = np.empty([1, 3000])
for _ in range(64):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    y.append(opic.cash_current[max_val])
    x.append(opic.time)
    max_cash = opic.cash_current[max_val]
    if (opic.time > 0):
        # plt.text(opic.time, opic.cash_current[max_val], max_val)
        maximum.put(opic.time - 1, max_cash)
        np_time.put(opic.time - 1, max_val)
    opic.visit(max_val)

y1 = maximum[0]
x1 = np_time[0]
##print(maximum[0])
indexes = peakutils.indexes(maximum[0], thres= 1.6 / max(maximum[0]))
#print(indexes)
#print(np_time[0][indexes], maximum[0][indexes])
#plt.plot(x1, y1, lw=0.4, alpha=1.0)
plt.plot(indexes, maximum[0][indexes])
print("Number of peaks: %s " % len(x1[indexes]))
# plt.figure(figsize=(10,6))
# pplot(x, y, indexes)
# plt.title('First estimate')
#
# peaks = peakutils.interpolate(np_time[0], maximum[0], ind= indexes)
# print(peaks)
# interpolatedIndexes = peakutils.interpolate(range(0, len(maximum[0])), maximum[0], ind=indexes)
# Print local maximums
plt.plot(x, y, linewidth=0.5)
plt.show()

pos = nx.spring_layout(G)

ppr = PPR(G)

for seed in np_time[0][indexes]:
    #seed = str(int(seed))
    if seed not in seeds:
        for v in G[seed]:
            if v in seeds:
                break
        seeds.append(seed)

print("Number of seeds: %s " % len(seeds))
print(seeds)

#seeds = []
#
#for i in range(389):
#    seed = str(randint(0, 1004))
#    if seed not in seeds:
#        for v in G[seed]:
#            if v in seeds:
#                break
#        seeds.append(seed)


community = {}
index = 0
for seed in seeds:
    best = ppr.PPRRank(G, 0.99, 0.01, [seed])
    community[seed] = best
    color = 'C' + str(index % 8)
    nx.draw_networkx_nodes(G, pos, best, node_color=color, node_size=150)
    index += 1

nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
nx.draw_networkx_edges(G, pos, width=0.5, color='grey')
plt.show()


exit()
# Ground truth

real_communities = imports.ground_truth('../data/ground-truth/eu-core')


stats = Stats(real_communities)
mean = stats.compare(community)

print("Mean accuracy %f" % mean)
print("Communites detected %s" % len(community))
print("Real Communites %s" % len(real_communities))

exit()

import matplotlib.pyplot as plt
import networkx as nx
from module.OPIC import OPIC
from module.PPR import PPR
from module.importData import ImportData
from module.stats import Stats

imports = ImportData()

G = imports.text_graph('../data/edgelist/eu-core')

options = {
    'node_size': 10,
    'line_color': 'grey',
    'linewidths': 0,
    'width': 0.05,
}

# G = nx.karate_club_graph()
opic = OPIC(G, 10)
opic.visit('390')

y = []
x = []
current_max = 0
i = 0
seeds = []
for _ in range(3000):
    max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
    y.append(opic.cash_current[max_val])
    x.append(opic.time)
    max_cash = opic.cash_current[max_val]
    if (opic.cash_current[max_val] > current_max - (max_cash * .08)) and opic.time > 1250:
        plt.text(opic.time, opic.cash_current[max_val], max_val)

        if max_val not in seeds:
            seeds.append(max_val)

        i += 1
    if opic.cash_current[max_val] > current_max:
        current_max = opic.cash_current[max_val]

    opic.visit(max_val)

# Print local maximums
plt.plot(x, y, linewidth=2.0)
plt.show()

pos = nx.spring_layout(G)

ppr = PPR(G)

community = {}
index = 0
for seed in seeds:
    best = ppr.PPRRank(G, 0.99, 0.0001, [seed])
    community[seed] = best
    color = 'C' + str(index % 8)
    nx.draw_networkx_nodes(G, pos, best, node_color=color, node_size=10)
    index += 1

#nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
#nx.draw_networkx_edges(G, pos, width=0.05, color='grey')
#plt.show()


# Ground truth

real_communities = imports.ground_truth('../data/ground-truth/eu-core')
stats = Stats(real_communities)
stats.compare(community)

print("Communites detected %s" % len(community))
print("Real Communites %s" % len(real_communities))

exit()


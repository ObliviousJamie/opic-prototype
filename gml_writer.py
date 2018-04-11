import networkx as nx

from module.LFR.readLFR import ReadLFR
from module.expansion.ppr import PPR
from module.expansion.neighborhood import NeighborExpand
from module.tools.extra.samples import Samples


def lfr_to_gml(reader, save_location, seeders):
    for seeder in seeders:
        lfr_dict = reader.read()
        for key, value in lfr_dict.items():
            size, mix, overlap = key
            graph, communities = value

            for vertex, membership in communities.items():
                graph.node[vertex]['community'] = membership
                graph.node[vertex]['roverlap'] = len(membership)

            if seeder:
                found_communities = find_communities(seeder, graph)
                for vertex, membership in found_communities.items():
                    graph.node[vertex]['bigdiscover'] = max(membership)
                    graph.node[vertex]['smalldiscover'] = min(membership)
                    graph.node[vertex]['foverlap'] = len(membership)

            loc = "%s_%s_%s_%s_%s.gml" % (save_location, size, mix, overlap, seeder.name)
            nx.write_gml(graph, loc)


def graph_to_gml(graph, save_location, seeders, real_communities=None):
    clean_graph = graph.to_undirected()
    for seeder in seeders:
        graph = clean_graph.to_undirected()
        found_communities = find_communities(seeder, graph)
        for vertex, membership in found_communities.items():
            graph.node[vertex]['bigdiscover'] = max(membership)
            graph.node[vertex]['smalldiscover'] = min(membership)
            graph.node[vertex]['foverlap'] = len(membership)

        if real_communities is not None:
            for membership, vertices in real_communities.items():
                for vertex in vertices:
                    graph.node[vertex]['community'] = membership

        loc = "%s_%s.gml" % (save_location, seeder.name)
        nx.write_gml(graph, loc)


def find_communities(seeder, graph):
    ppr = PPR()
    communities = {}

    print("Seeding...", seeder.name)
    seeds = seeder.seed(graph)
    print("Seeds...", len(seeds))

    #TODO doesnt this just expand neighborhood not seeds!
    expander = NeighborExpand(graph)
    expanded_seeds = expander.expand_seeds(seeds)
    print("Expanded seeds...", len(expanded_seeds))

    community_count = 0
    size_tuples = []

    for center_seed, neighbor_seeds in expanded_seeds.items():
        detected = ppr.ppr_rank(graph, neighbor_seeds)
        graph.node[center_seed]['cseed'] = str(community_count)
        for seed in neighbor_seeds:
            graph.node[seed]['nseed'] = str(community_count)

        if len(detected) > 2:
            size_tuples.append((len(detected), detected))
            community_count += 1

    print(f"Communities discovered = {community_count}")

    community_count = 0
    size_tuples = sorted(size_tuples)
    print(size_tuples)
    for _, detected in size_tuples:
        for v in detected:
            communities.setdefault(v, [])
            communities[v].append(str(community_count))
        community_count += 1

    return communities


mix_opic = Samples().seeders_mix('opic')
mix_min = Samples().seeders_mix('mfcmin')
mix_mfcopic = Samples().seeders_mix('mfcopic')
all = [mix_opic, mix_min, mix_mfcopic]
all = [Samples().seeders('ppr')]

reader = ReadLFR([1000], [0.1], overlapping_fractions=[0.1])
fb = nx.read_pajek("/home/jmoreland/Downloads/graphs/fb.net")

for seeders in all:
    #    fb = nx.read_pajek("/home/jmoreland/Downloads/graphs/fb.net")
    lfr_to_gml(reader, '/home/jmoreland/Documents/PRJ/small', seeders)
#    graph_to_gml(fb, '/home/jmoreland/Documents/PRJ/fb', seeders)



# ./gml_writer.py -s 5000 -m 0.1 -o 0.1 -c standard
# ./gml_writer.py -d ../data.txt -t ../truth.txt -c standard

# -c -- standard, all, mfcopic

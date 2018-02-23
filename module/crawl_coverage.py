from module.LFR.readLFR import ReadLFR
from module.graph.tools.graph_clean import GraphClean
from module.imports.importData import ImportData
from module.statistics.crawl_coverage_plot import CrawlCoverage


def flip_list_dict(dictionary):
    new_dict = {}
    for key, value_list in dictionary.items():
        for item in value_list:
            new_dict.setdefault(item, list())
            new_dict[item].append(key)
    return new_dict


reader = ReadLFR([1000], [0.1, 0.3], overlapping_fractions=[0.1, 0.2, 0.3, 0.4, 0.5])
lfr_dict = reader.read()
for key, value in lfr_dict.items():
    reverse = {}
    graph, community = value
    for vertex, members in community.items():
        for community_key in members:
            reverse.setdefault(community_key, [])
            reverse[community_key].append(vertex)
    print()
    print()
    print(key)
    crawl = CrawlCoverage()
    crawl.coverage_plot(graph, reverse, community)

crawl = CrawlCoverage()
imports = ImportData()
I = imports.text_graph('../data/edgelist/eu-core')
cleaner = GraphClean()
I = cleaner.prune_unconnected_components(I)

real_communities = imports.ground_truth('../data/ground-truth/eu-core')
membership = flip_list_dict(real_communities)
crawl.coverage_plot(I, real_communities, membership)

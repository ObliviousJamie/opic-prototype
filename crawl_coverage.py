import matplotlib.pyplot as plt
from module.graph.tools.graph_clean import GraphClean
from module.import_options import Options
from module.statistics.crawl_coverage_plot import CrawlCoverage


class CrawlCoverageManager:

    def __init__(self, crawl_coverage, save_base):
        self.crawl_coverage = crawl_coverage
        self.save_base = save_base

    def coverage_lfr(self, reader):
        lfr_dict = reader.read()
        for key, value in lfr_dict.items():
            graph, community = value
            flip_community = self.flip_list_dict(community)
            self.crawl_coverage.coverage_plot(graph, flip_community, community)
            size, mix, overlap = key
            plt.savefig(f"{self.save_base}_{size}_{mix}_{overlap}.png")
            plt.close()

    def coverage_real(self, graph, communities):
        cleaner = GraphClean()
        cleaner.prune_unconnected_components(graph)
        flip_community = self.flip_list_dict(communities)
        self.crawl_coverage.coverage_plot(graph, flip_community, communities)
        plt.savefig(f"{self.save_base}_custom_graph.png")
        plt.show()
        plt.close()

    @staticmethod
    def flip_list_dict(dictionary):
        new_dict = {}
        for key, value_list in dictionary.items():
            for item in value_list:
                new_dict.setdefault(item, list())
                new_dict[item].append(key)
        return new_dict

if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv)
    seeders = option_import.select_seeders()

    directory = os.getcwd()
    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/crawl_coverage_{date}"

    reader = option_import.generate_reader()
    crawl_manager = CrawlCoverageManager(CrawlCoverage(), save_name)
    if reader is not None:
        crawl_manager.coverage_lfr(reader)
    else:
        graph, communities = option_import.import_real(directory, need_truth=True)
        print("Graph and community imported")
        crawl_manager.coverage_real(graph, communities)


# ./crawl_coverage.py -s 5000 -m 0.1 -o 0.1
# ./crawl_coverage.py -d ../data.txt


import matplotlib.pyplot as plt
from module.tools.extra.graph_clean import GraphClean
from module.import_options import Options
from module.statistics.plots.crawl_coverage_plot import CrawlCoverage


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

            plt.legend()

            if len(key) is 2:
                size, mix = key
                plt.title(f"Benchmark network (mix: {mix} size: {size} overlap: None)")
                plt.savefig(f"{self.save_base}_{size}_{mix}.png")
            else:
                size, mix, overlap = key
                plt.title(f"Benchmark network (mix: {mix} size: {size} overlap: {overlap})")
                plt.savefig(f"{self.save_base}_{size}_{mix}_{overlap}.png")

            plt.close()

    def coverage_real(self, graph, communities):
        name = "custom name"
        cleaner = GraphClean()
        cleaner.prune_unconnected_components(graph)
        flip_community = self.flip_list_dict(communities)
        self.crawl_coverage.coverage_plot(graph, communities, flip_community)
        plt.legend()
        plt.title(f"{name}")
        plt.savefig(f"{self.save_base}_{name}.png")
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

    option_import = Options(argv, parameters="smocdt")
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

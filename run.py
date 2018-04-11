"""
Runs a choice of CD-OPIC, CD-MFCOPIC or CD-MFC with parameters.
This will output a text file with found communities.
"""
from module.import_options import Options
from module.lfr.helper import LFRHelper
from module.tools.extra.expand_seeds import SeedExpansion
from module.tools.extra.read_seeds import SeedReader


class Run:

    def __init__(self, seeders, save_location):
        self.seeders = seeders
        self.save_location = save_location

    def run(self, network, gseeds, label=''):
        expander = SeedExpansion()

        expanded_communities = expander.expand(G=network, seeds=gseeds)

        date = datetime.datetime.now().strftime("%y-%m-%H%S")
        name = f"{self.save_location}_{label}_{date}.dat"

        print(f"Writing produced communities to {name}")

        with open(name, "w") as file:
            for _, community in expanded_communities.items():
                string_community = " ".join(community)
                print(string_community, file=file)

    def seeder_run(self, network, label='custom_graph'):
        for seeder in self.seeders:
            seeder_seeds = seeder.seed(network)
            seed_label = f"{seeder.name}_{label}"
            self.run(network, seeder_seeds, label=seed_label)

    def lfr_run(self, lfr_reader):
        lfr_dict = lfr_reader.read()
        for key, value in lfr_dict.items():
            size, mix, overlap = LFRHelper.extract_key(key)
            network, _ = value
            self.seeder_run(network, label=f"{size}_{mix}_{overlap}")


if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv, parameters="smocdl")
    seeders = option_import.select_seeders()

    directory = os.getcwd()
    save_name = f"{directory}/output"

    run = Run(seeders, save_name)

    reader = option_import.generate_reader()
    if reader is not None:
        run.lfr_run(reader)
    else:
        graph, communities = option_import.import_real(directory, need_truth=False)
        print("Graph and community imported")
        seed_list = option_import.find_seed_list()
        if seed_list is not None:
            seed_file_location = f"{directory}/{seed_list}"
            seed_reader = SeedReader(seed_list)
            seeds = seed_reader.read()
            run.run(graph, seeds)
        else:
            run.seeder_run(graph)

from module.import_options import Options
from module.seeding.seeder.spreadhub import Spreadhub
from module.statistics.fscore.fscorecalculator import FscoreCalculator

if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv, parameters="smocd")

    seeders = option_import.select_seeders()

    directory = os.getcwd()
    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/average_scores{date}_all"

    calculator = FscoreCalculator(seeders, save_name)

    reader = option_import.generate_reader()
    if reader is not None:
        seeders.append(Spreadhub(int(float(reader.network_sizes[0]) * 0.2)))
        calculator.lfr_fscores(reader)
    else:
        graph, communities = option_import.import_real(directory, need_truth=True)
        print("Graph and community imported")
        seeders.append(Spreadhub(int(float(len(graph.nodes)) * 0.2)))
        rows = calculator.imported_fscores(graph, communities, label='graph')
        for name, score in rows:
            print(f"Seeder: {name}   F1: {score[0]}     F2: {score[1]}")

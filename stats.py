from module.graph.tools.samples import Samples
from module.import_options import Options
from module.seeding.spreadhub_seed import Spreadhub
from module.statistics.fscorecalculator import FscoreCalculator

if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv)
    #TODO change back
    seeders = option_import.select_seeders()
    #samps = Samples()
    #seeders1 = samps.every_mfcopic()
    #seeders2 = samps.every_minmfc()
    #seeders3 = samps.every_opic()
    #seeders = []
    #seeders.extend(seeders1)
    #seeders.extend(seeders2)
    #seeders.extend(seeders3)
    #size = len(seeders)
    #print(f"All seeders = {size * 6}")

    #seeders = samps.varied(1000)
    size = len(seeders)

    print(f"Vertex seeders {size}")


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
        if rows is not None:
            print("Printed rows")

# ./stats.py -s 5000 -m 0.1 -o 0.1 -c standard
# ./stats.py -d ../data.txt -t ../truth.txt -c standard

# -c -- standard, all, mfcopic


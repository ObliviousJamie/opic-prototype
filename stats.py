from module.import_options import Options
from module.statistics.fscorecalculator import FscoreCalculator

if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv)
    seeders = option_import.select_seeders()

    directory = os.getcwd()
    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/f_scores{date}.csv"

    calculator = FscoreCalculator(seeders, save_name)

    reader = option_import.generate_reader()
    if reader is not None:
        calculator.lfr_fscores(reader)
    else:
        graph, communities = option_import.import_real(directory, need_truth=True)
        print("Graph and community imported")
        rows = calculator.imported_fscores(graph, communities, label='graph')
        if rows is not None:
            print("Printed rows")

# ./stats.py -s 5000 -m 0.1 -o 0.1 -c standard
# ./stats.py -d ../data.txt -t ../truth.txt -c standard

# -c -- standard, all, mfcopic

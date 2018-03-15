from module.import_options import Options
from module.statistics.fscorecalculator import FscoreCalculator
from module.LFR.readLFR import ReadLFR
from module.graph.tools.samples import Samples

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
        graph, communities = option_import.import_real(need_truth=True)
        print('Ground truth functionality not yet added')

exit()

reader = ReadLFR([1000, 5000], [0.1], overlapping_fractions=[0.1])
reader_large = ReadLFR([50000], [0.1], overlapping_fractions=[0.1])
reader_varied = ReadLFR([1000, 5000], [0.1, 0.3], overlapping_fractions=[0.1, 0.5])

ppr = Samples().seeders('ppr')
mfcopic = Samples().mfcopic_peak_variety(2.0, 0.5)
sensitivity = Samples().custom()

# lfr_fscores(reader, mfcopic)
save = '/home/jmoreland/Documents/PRJ/sensitivity'
plotter = FscoreCalculator(mfcopic, f"{save}/seed_select_methods.csv")
plotter.lfr_fscores(reader)
# plotter.lfr_fscores(reader, f"{save}/threshold_variance_5000.csv")
# plotter.lfr_fscores(reader_large, f"{save}/threshold_variance_50000.csv")


# ./stats.py -s 5000 -m 0.1 -o 0.1 -c standard
# ./stats.py -d ../data.txt -t ../truth.txt -c standard

# -c -- standard, all, mfcopic

from module.import_options import Options
from module.statistics.plots.seed_plot import SeedPlot

if __name__ == '__main__':
    from sys import argv
    import os
    import datetime

    option_import = Options(argv, parameters="smoc")
    seeders = option_import.select_seeders()

    directory = os.getcwd()
    date = datetime.datetime.now().strftime("%y-%m-%H%S")
    save_name = f"{directory}/crawl_coverage_{date}"

    reader = option_import.generate_reader()
    if reader is not None:
        seed_plot = SeedPlot(reader)
        seed_plot.plot_fscore(1, seeders)
    else:
        print("seeds.py does not support custom input")

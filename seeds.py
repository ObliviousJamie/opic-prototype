from module.LFR.readLFR import ReadLFR
from module.graph.tools.samples import Samples
from module.statistics.seed_plot import SeedPlot

if __name__ == '__main__':
    reader = ReadLFR([1000], [0.3])

    seed_plot = SeedPlot(reader)
    samps = Samples()
    seeders = samps.every_mfcopic()
    seeders.extend(samps.every_opic())
    seed_plot.plot_fscore(1, seeders)
    #seed_plot.plot_fscore(1)

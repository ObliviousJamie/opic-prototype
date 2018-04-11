from module.LFR.plotLFR import PlotLFR
from module.LFR.readLFR import ReadLFR
from module.LFR.writeLFR import WriteLFR
from module.graph.tools.samples import Samples
from module.seeding.PPRFilter import PPRFilter
from module.seeding.mfc_min_seed import SeedMinMFC
from module.seeding.mfc_opic_seed import SeedMFCOPIC
from module.seeding.opic_seed import SeedOPIC
from module.seeding.seed_filter import DefaultFilter
from module.seeding.spreadhub_seed import Spreadhub


def plot(seeders, reader, added_loc=''):
    lfr = WriteLFR(reader)
    for seeder in seeders:
        lfr.calculate_communities(seeder)
    lfr.calculate_mfc()

    plot_tuples = []
    for seeder in seeders:
        method_tup = (seeder.name, seeder.threshold)
        plot_tuples.append(method_tup)
    plot_tuples.append(("mfc-original",0))

    save = (f"/home/jmoreland/Pictures/PRJ{added_loc}")
    lfr_plot = PlotLFR(plot_tuples, save_loc=save)
    #lfr_plot.plot([1000], [0.1, 0.3], [0.1, 0.2, 0.3, 0.4, 0.5])
    lfr_plot.plot(reader.network_sizes, reader.mixing_parameters, reader.overlapping_fractions)

def plot_nowrite(seeders, reader, added_loc=''):
    #lfr = WriteLFR(reader)
    #for seeder in seeders:
    #    lfr.calculate_communities(seeder)

    plot_tuples = []
    for seeder in seeders:
        method_tup = (seeder.name, seeder.threshold)
        plot_tuples.append(method_tup)

    save = (f"/home/jmoreland/Pictures/PRJ{added_loc}")
    lfr_plot = PlotLFR(plot_tuples, save_loc=save)
    #lfr_plot.plot([1000], [0.1, 0.3], [0.1, 0.2, 0.3, 0.4, 0.5])
    lfr_plot.plot(reader.network_sizes, reader.mixing_parameters, reader.overlapping_fractions)



seeders_normal = [SeedOPIC(1.8, return_type='string'), SeedMinMFC(2.0, return_type='string'),
                  SeedMFCOPIC(1.6, return_type='string'), Spreadhub(40, return_type='string')]

f_filter = DefaultFilter()
seeders_filtered = [SeedOPIC(1.0, return_type='string', s_filter=f_filter),
                    SeedMinMFC(1.0, return_type='string', s_filter=f_filter),
                    SeedMFCOPIC(1.0, return_type='string', s_filter=f_filter), Spreadhub(40, return_type='string')]

f_filter = PPRFilter(0.001)
seeders_filtered2 = [SeedOPIC(1.0, return_type='string', s_filter=f_filter),
                     SeedMinMFC(1.0, return_type='string', s_filter=f_filter),
                     SeedMFCOPIC(1.0, return_type='string', s_filter=f_filter), Spreadhub(40, return_type='string')]

#reader = ReadLFR([1000], [0.1], overlapping_fractions=[0.1])

#plot(seeders_normal, reader)
#plot(seeders_filtered, reader, '/nmi_neighbor')
#plot(seeders_filtered2, reader, '/nmi_ppr')
samples = Samples()
everymfc = samples.every_mfcopic()
everyopic = samples.every_opic()
everymin = samples.every_minmfc()
standard = samples.standard()

#reader = ReadLFR([1000], [0.1], overlapping_fractions=[0.1, 0.3, 0.5])
#plot(seeders_normal,reader, '/everymfcopic')
#exit()

reader = ReadLFR([1000], [0.1], overlapping_fractions=[0.1, 0.3, 0.5])
plot(standard, reader, '/all_nmi')
#plot(everymfc, reader, '/everymfcopic')
#plot(everymin, reader, '/everyminmfc')
#plot(everyopic, reader, '/everyopic')
#
#reader = ReadLFR([5000], [0.1], overlapping_fractions=[0.1,0.3,0.5])
#plot(everymfc, reader, '/everymfcopic')
#plot(everymin, reader, '/everyminmfc')
#plot(everyopic, reader, '/everyopic')

#reader = ReadLFR([1000], [0.3], overlapping_fractions=[0.1,0.3,0.5])
#plot(everymfc, reader, '/everymfcopic')
#plot(everymin, reader, '/everyminmfc')
#plot(everyopic, reader, '/everyopic')
#
#reader = ReadLFR([5000], [0.3], overlapping_fractions=[0.1,0.3,0.5])
#plot(everymfc, reader, '/everymfcopic')
#plot(everymin, reader, '/everyminmfc')
#plot(everyopic, reader, '/everyopic')

#reader = ReadLFR([1000, 5000], [0.1], overlapping_fractions=[0.1])
#plot_nowrite(everymfc, reader, '/everymfcopic')
#plot_nowrite(everymin, reader, '/everyminmfc')
#plot_nowrite(everyopic, reader, '/everyopic')


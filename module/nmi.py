from module.LFR.plotLFR import PlotLFR
from module.LFR.readLFR import ReadLFR
from module.LFR.writeLFR import WriteLFR
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

    plot_tuples = []
    for seeder in seeders:
        method_tup = (seeder.name, seeder.threshold)
        plot_tuples.append(method_tup)

    save = (f"/home/jmoreland/Pictures/PRJ{added_loc}")
    lfr_plot = PlotLFR(plot_tuples, save_loc=save)
    lfr_plot.plot([1000], [0.1, 0.3], [0.1, 0.2, 0.3, 0.4, 0.5])


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

reader = ReadLFR([1000], [0.1, 0.3], overlapping_fractions=[0.1, 0.2, 0.3, 0.4, 0.5])

plot(seeders_normal, reader)
plot(seeders_filtered, reader, '/nmi_neighbor')
plot(seeders_filtered2, reader, '/nmi_ppr')

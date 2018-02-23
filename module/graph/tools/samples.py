from module.seeding import *
from module.seeding.PPRFilter import PPRFilter
from module.seeding.mfc_min_seed import SeedMinMFC
from module.seeding.mfc_opic_seed import SeedMFCOPIC
from module.seeding.opic_seed import SeedOPIC
from module.seeding.seed_filter import DefaultFilter
from module.seeding.spreadhub_seed import Spreadhub


class Samples:

    def seeders(self, type='normal'):
        seeders_normal = [SeedOPIC(1.5, return_type='string'), SeedMinMFC(2.6, return_type='string'),
                  SeedMFCOPIC(2.1, return_type='string'), Spreadhub(40, return_type='string')]
        f_filter = DefaultFilter()
        seeders_filtered = [SeedOPIC(1.5, return_type='string', s_filter=f_filter),
                    SeedMinMFC(2.6, return_type='string', s_filter=f_filter),
                    SeedMFCOPIC(2.1, return_type='string', s_filter=f_filter), Spreadhub(40, return_type='string')]

        f_filter = PPRFilter(0.001)
        seeders_filtered2 = [SeedOPIC(1.5, return_type='string', s_filter=f_filter),
                     SeedMinMFC(1.5, return_type='string', s_filter=f_filter),
                     SeedMFCOPIC(2.1, return_type='string', s_filter=f_filter), Spreadhub(40, return_type='string')]

        if type is 'ppr':
            return seeders_filtered2
        elif type is 'neighbor':
            return seeders_filtered
        else:
            return seeders_normal

    def seeders_mix(self, type='mfcmin'):
        f_filter_neighbor = DefaultFilter()
        f_filter_ppr = PPRFilter(0.0001)

        opic_thres = 1.9
        seeders_opic = [SeedOPIC(opic_thres, return_type='string'), SeedOPIC(opic_thres, return_type='string', s_filter=f_filter_neighbor),
                          SeedOPIC(opic_thres, return_type='string', s_filter=f_filter_ppr)]

        seeders_mfcopic = [SeedMFCOPIC(2.1, return_type='string'), SeedMFCOPIC(0.1, return_type='string', s_filter=f_filter_neighbor),
                        SeedMFCOPIC(0.1, return_type='string', s_filter=f_filter_ppr)]

        seeders_mfcmin = [SeedMinMFC(2.0, return_type='string'), SeedMinMFC(0.1, return_type='string', s_filter=f_filter_neighbor),
                        SeedMinMFC(0.1, return_type='string', s_filter=f_filter_ppr)]

        if type is 'opic':
            return seeders_opic
        elif type is 'mfcopic':
            return seeders_mfcopic
        else:
            return seeders_mfcmin


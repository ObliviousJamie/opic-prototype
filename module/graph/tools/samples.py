from module.seeding import *
from module.seeding.PPRFilter import PPRFilter
from module.seeding.basic_peak_finder import PeakFinder
from module.seeding.mfc_min_seed import SeedMinMFC
from module.seeding.mfc_opic_seed import SeedMFCOPIC
from module.seeding.opic_seed import SeedOPIC
from module.seeding.seed_filter import DefaultFilter
from module.seeding.spreadhub_seed import Spreadhub
from module.seeding.window_peak_finder import WindowPeakFinder


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
                     SeedMFCOPIC(2.0, return_type='string', s_filter=f_filter), Spreadhub(200, return_type='string')]

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

    def mfcopic_peak_variety(self, threshold, peak_threshold):
        f_filter_ppr = PPRFilter(0.0001)
        basic_peak = PeakFinder(0.3)
        avg_peak = WindowPeakFinder(0.3, 20)
        seeders_mfcmin = [SeedMFCOPIC(threshold, return_type='string', s_filter=f_filter_ppr, start='1'),
                          SeedMFCOPIC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=basic_peak, start='1'),
                          SeedMFCOPIC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=avg_peak, start='1')]

        return seeders_mfcmin

    def threshold_sensitivity(self):
        f_filter_ppr = PPRFilter(0.0001)
        seeders = []
        for i in range(1, 11):
            print(f"Trying {i / 10}")
            avg_peak = WindowPeakFinder((i /10), 20)
            basic_peak = PeakFinder(i / 10)
            mfcopic = SeedMFCOPIC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=avg_peak, start='1')
            minmfc = SeedMinMFC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=avg_peak, start='1')
            mfcopicv2 = SeedMFCOPIC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=basic_peak, start='1')
            minmfcv2 = SeedMinMFC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=basic_peak, start='1')
            seeders.append(mfcopic)
            seeders.append(minmfc)
            seeders.append(mfcopicv2)
            seeders.append(minmfcv2)

        return seeders

    def every_minmfc(self):
        seeders = []
        f_filter_ppr = PPRFilter(0.0001)
        f_filter_neighbor = DefaultFilter()

        for i in range(1, 11):
            avg_peak = WindowPeakFinder((i /10), 20)
            basic_peak = PeakFinder(i / 10)

            avg_ppr = SeedMinMFC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=avg_peak, start='1')
            basic_ppr = SeedMinMFC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=basic_peak, start='1')

            avg_neigh = SeedMinMFC(0, return_type='string', s_filter=f_filter_neighbor, peak_filter=avg_peak, start='1')
            basic_neigh = SeedMinMFC(0, return_type='string', s_filter=f_filter_neighbor, peak_filter=basic_peak, start='1')

            basic = SeedMinMFC(0, return_type='string', peak_filter=basic_peak, start='1')
            avg = SeedMinMFC(0, return_type='string', peak_filter=avg_peak, start='1')

            seeders.append(basic)
            seeders.append(avg)

            seeders.append(avg_ppr)
            seeders.append(basic_ppr)
            seeders.append(avg_neigh)
            seeders.append(basic_neigh)

        for i in range(1, 28):
            adjusted = i /10
            plain = SeedMinMFC(adjusted, return_type='string', start='1')
            neigh = SeedMinMFC(adjusted, return_type='string', s_filter=f_filter_ppr, start='1')
            ppr = SeedMinMFC(adjusted, return_type='string', s_filter=f_filter_neighbor, start='1')
            seeders.append(plain)
            seeders.append(neigh)
            seeders.append(ppr)

        return seeders


    def every_opic(self):
        seeders = []
        f_filter_ppr = PPRFilter(0.0001)
        f_filter_neighbor = DefaultFilter()

        for i in range(0, 28):
            adjusted = i /10
            plain = SeedOPIC(adjusted, return_type='string', start='1')
            neigh = SeedOPIC(adjusted, return_type='string', s_filter=f_filter_ppr, start='1')
            ppr = SeedOPIC(adjusted, return_type='string', s_filter=f_filter_neighbor, start='1')
            seeders.append(plain)
            seeders.append(neigh)
            seeders.append(ppr)

        return seeders


    def every_mfcopic(self):
        seeders = []
        f_filter_ppr = PPRFilter(0.0001)
        f_filter_neighbor = DefaultFilter()

        for i in range(1, 11):
            avg_peak = WindowPeakFinder((i /10), 20)
            basic_peak = PeakFinder(i / 10)

            avg_ppr = SeedMFCOPIC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=avg_peak, start='1')
            basic_ppr = SeedMFCOPIC(0, return_type='string', s_filter=f_filter_ppr, peak_filter=basic_peak, start='1')

            avg_neigh = SeedMFCOPIC(0, return_type='string', s_filter=f_filter_neighbor, peak_filter=avg_peak, start='1')
            basic_neigh = SeedMFCOPIC(0, return_type='string', s_filter=f_filter_neighbor, peak_filter=basic_peak, start='1')

            basic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak, start='1')
            avg = SeedMFCOPIC(0, return_type='string', peak_filter=avg_peak, start='1')

            seeders.append(basic)
            seeders.append(avg)
            seeders.append(avg_ppr)
            seeders.append(basic_ppr)
            seeders.append(avg_neigh)
            seeders.append(basic_neigh)

        for i in range(0, 28):
            adjusted = i /10
            plain = SeedMFCOPIC(adjusted, return_type='string', start='1')
            neigh = SeedMFCOPIC(adjusted, return_type='string', s_filter=f_filter_ppr, start='1')
            ppr = SeedMFCOPIC(adjusted, return_type='string', s_filter=f_filter_neighbor, start='1')
            seeders.append(plain)
            seeders.append(neigh)
            seeders.append(ppr)

        return seeders


    def standard(self):
        basic_peak = PeakFinder(0.1)
        mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak)
        minmfc = SeedMinMFC(1.0, return_type='string')
        return [mfcopic, minmfc]

    def mfcopic(self):
        basic_peak = PeakFinder(0.1)
        mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak)
        return [mfcopic]

    def all(self):
        basic_peak = PeakFinder(0.1)
        mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak)
        minmfc = SeedMinMFC(1.0, return_type='string')
        opic = SeedOPIC(1.5, return_type='string')
        return [mfcopic, minmfc, opic]

    def varied(self, size):
        basic_peak = PeakFinder(0.1)

        seeders = []

        for i in range(1,size):
            mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak, start=str(i), label=f"MFCOPIC  vertex {i}")
            minmfc = SeedMinMFC(1.0, return_type='string', start=str(i), label=f"MinMFC  vertex {i}")
            opic = SeedOPIC(1.5, return_type='string', start=str(i), label=f"OPIC  vertex {i}")

            if i % 2 == 0:
                seeders.append(mfcopic)
                seeders.append(minmfc)
                seeders.append(opic)
        return seeders















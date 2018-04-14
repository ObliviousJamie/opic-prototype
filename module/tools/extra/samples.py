from module.seeding.filter.neighborhood_filter import NeighborhoodFilter
from module.seeding.peak.basic_peak_finder import PeakFinder
from module.seeding.seeder.alternative.mfc_minhub_seed import SeedMinhubMFC
from module.seeding.seeder.alternative.opichub_seed import SeedOPICHub
from module.seeding.seeder.cd_mfc import SeedMFC
from module.seeding.seeder.cd_mfcopic import SeedMFCOPIC
from module.seeding.seeder.cd_opic import SeedOPIC


class Samples:

    @staticmethod
    def opic():
        opic = SeedOPIC(1.5, return_type='string')
        return [opic]

    @staticmethod
    def mfc():
        minmfc = SeedMFC(1.0, return_type='string')
        return [minmfc]

    @staticmethod
    def mfcopic():
        basic_peak = PeakFinder(0.1)
        mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak)
        return [mfcopic]

    @staticmethod
    def all():
        basic_peak = PeakFinder(0.1)
        mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak)
        minmfc = SeedMFC(1.0, return_type='string')
        opic = SeedOPIC(1.5, return_type='string')
        return [mfcopic, minmfc, opic]

    @staticmethod
    def quick():
        n_filter = NeighborhoodFilter()
        mfcopic = SeedMFCOPIC(2.5, return_type='string', s_filter=n_filter)
        minmfc = SeedMFC(1.4, s_filter=n_filter, return_type='string')
        opic = SeedOPIC(1.9, s_filter=n_filter, return_type='string')
        return [mfcopic, minmfc, opic]

    @staticmethod
    def alternative():
        minhub = SeedMinhubMFC(500, return_type='string')
        opichub = SeedOPICHub(500, return_type='string')
        return [minhub, opichub]

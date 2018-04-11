from module.seeding.peak.basic_peak_finder import PeakFinder
from module.seeding.seeder.cd_mfc import SeedMFC
from module.seeding.seeder.cd_mfcopic import SeedMFCOPIC
from module.seeding.seeder.cd_opic import SeedOPIC


class Samples:

    @staticmethod
    def standard():
        basic_peak = PeakFinder(0.1)
        mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak)
        minmfc = SeedMFC(1.0, return_type='string')
        return [mfcopic, minmfc]

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

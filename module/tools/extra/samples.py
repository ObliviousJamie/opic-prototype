from module.seeding.basic_peak_finder import PeakFinder
from module.seeding.mfc_min_seed import SeedMinMFC
from module.seeding.mfc_opic_seed import SeedMFCOPIC
from module.seeding.opic_seed import SeedOPIC


class Samples:

    @staticmethod
    def standard():
        basic_peak = PeakFinder(0.1)
        mfcopic = SeedMFCOPIC(0, return_type='string', peak_filter=basic_peak)
        minmfc = SeedMinMFC(1.0, return_type='string')
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
        minmfc = SeedMinMFC(1.0, return_type='string')
        opic = SeedOPIC(1.5, return_type='string')
        return [mfcopic, minmfc, opic]

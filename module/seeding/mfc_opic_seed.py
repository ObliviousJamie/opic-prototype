import numpy as np

from module.crawling.mfc import MFC
from module.crawling.opic import OPIC
from module.seeding.threshold_seed import ThresholdSeeder


class SeedMFCOPIC(ThresholdSeeder):

    def __init__(self, threshold, label=None, start=None, return_type="integer", s_filter=None, peak_filter=None):
        super(SeedMFCOPIC, self).__init__(threshold=threshold, return_type=return_type, s_filter=s_filter, peak_filter=peak_filter)
        self.start = start

        if label is None:
            self._gen_name("MFCOPIC")
        else:
            self.name = label

    def seed(self, G):
        start = self.start
        if start is None:
            start = self.random_vertex(G)

        mfc = MFC(G, start)

        opic = OPIC(G)
        opic.visit(start)

        x_axis, y_axis = [], []
        seeds = []

        while not mfc.empty():
            max_val = mfc.next()
            current_cash = opic.cash_current[max_val]

            if self.peak_filter is not None:
                if self.peak_filter.is_peak(current_cash):
                    seeds.append(max_val)

            if opic.time > 0:
                x_axis.append(max_val)
                y_axis.append(current_cash)
            opic.visit(max_val)

        y_axis = np.array(y_axis)
        x_axis = np.array(x_axis)

        if self.peak_filter is None:
            seeds = self.pick_peaks(x_axis, y_axis, G)

        if self.s_filter is not None:
            seeds = self.s_filter.filter(seeds, G)

        return seeds

import numpy as np

from module.crawling.MFC import MFC
from module.crawling.OPIC import OPIC
from module.seeding.threshold_seed import ThresholdSeeder


class SeedMFCOPIC(ThresholdSeeder):

    def __init__(self, threshold, start=None, return_type="integer", s_filter=None):
        super(SeedMFCOPIC, self).__init__(threshold=threshold, return_type=return_type)
        self.start = start
        self.s_filter = s_filter
        self.name = 'MFCOPIC'
        if s_filter is not None:
            self.name = f'{self.name}_{s_filter.name}'

    def seed(self, G):
        start = self.start
        if start is None:
            start = self.random_vertex(G)

        mfc = MFC(G, start)

        opic = OPIC(G, 40)
        opic.visit(start)

        x_axis, y_axis = [], []

        while not mfc.empty():
            max_val = mfc.next()
            current_cash = opic.cash_current[max_val]

            if opic.time > 0:
                x_axis.append(max_val)
                y_axis.append(current_cash)
            opic.visit(max_val)

        y_axis = np.array(y_axis)
        x_axis = np.array(x_axis)

        seeds = self.pick_peaks(x_axis, y_axis, G)

        if self.s_filter is not None:
            seeds = self.s_filter.filter(seeds, G)

        return seeds

import numpy as np

from module.crawling.MFC import MFC
from module.seeding.threshold_seed import ThresholdSeeder


class SeedMinMFC(ThresholdSeeder):

    def __init__(self, threshold, label=None, start=None, return_type="integer", s_filter=None, peak_filter=None):
        super(SeedMinMFC, self).__init__(threshold=threshold, return_type=return_type, s_filter=s_filter, peak_filter=peak_filter)
        self.start = start

        if label is None:
            self._gen_name("MinPeakMFC")
        else:
            self.name = label

    def seed(self, G):
        start = self.start
        if start is None:
            start = self.random_vertex(G)

        mfc = MFC(G, start)

        x = []
        seeds = []

        while not mfc.empty():
            max_vertex = mfc.next()
            x.append(max_vertex)
            if self.peak_filter is not None:
                if mfc.y[-1] != 0 and self.peak_filter.is_peak((1 / mfc.y[-1])):
                    seeds.append(max_vertex)

        if self.peak_filter is None:
            print('Running gaussian peak detections')
            y_axis = []
            for ref in mfc.y:
                if ref == 0:
                    y_axis.append(0)
                else:
                    y_axis.append(1 / ref)

            x_axis = np.array(x)
            y_axis = np.array(y_axis)
            seeds = self.pick_peaks(x_axis, y_axis, G)

        if self.s_filter is not None:
            seeds = self.s_filter.filter(seeds, G)

        return seeds

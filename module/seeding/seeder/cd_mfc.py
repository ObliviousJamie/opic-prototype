import numpy as np

from module.crawling.mfc import MFC
from module.seeding.seed_progress import SeedProgress
from module.seeding.seeder.threshold_seed import ThresholdSeeder


class SeedMFC(ThresholdSeeder):

    def __init__(self, threshold=1.0, label=None, start=None, return_type="integer", s_filter=None, peak_filter=None):
        super(SeedMFC, self).__init__(threshold=threshold, return_type=return_type, s_filter=s_filter,
                                      peak_filter=peak_filter)
        self.start = start

        if label is None:
            self._gen_name("CD-MFC")
        else:
            self.name = label

    def seed(self, G):
        progress = SeedProgress(G, label=self.name)

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
                if mfc.max_references[-1] != 0 and self.peak_filter.is_peak((1 / mfc.max_references[-1])):
                    seeds.append(max_vertex)

            progress.update()

        if self.peak_filter is None:
            y_axis = []
            for ref in mfc.max_references:
                if ref == 0:
                    y_axis.append(0)
                else:
                    y_axis.append(1 / ref)

            x_axis = np.array(x)
            y_axis = np.array(y_axis)
            seeds = self.pick_peaks(x_axis, y_axis, G)

        if self.s_filter is not None:
            seeds = self.s_filter.filter(seeds, G)

        progress.finish()

        return seeds

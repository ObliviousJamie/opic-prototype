import peakutils
import numpy as np

from module.MFC import MFC
from module.seeding.threshold_seed import ThresholdSeeder


class SeedMinMFC(ThresholdSeeder):

    def __init__(self, threshold, start=None, return_type="integer"):
        super(SeedMinMFC, self).__init__(threshold=threshold, return_type=return_type)
        self.start = start

    def seed(self, G):
        start = self.start
        if start is None:
            start = self.random_vertex(G)

        mfc = MFC(G, start)

        x = []

        while not mfc.empty():
            max_vertex = mfc.next()
            x.append(max_vertex)

        y_axis = []
        for ref in mfc.y:
            if ref == 0:
                y_axis.append(0)
            else:
                y_axis.append(1 / ref)

        x_axis = np.array(x)
        y_axis = np.array(y_axis)

        seeds = self.pick_peaks(x_axis, y_axis, G)

        return seeds
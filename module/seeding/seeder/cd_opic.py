import numpy as np

from module.crawling.opic import OPIC
from module.seeding.seed_progress import SeedProgress
from module.seeding.seeder.threshold_seed import ThresholdSeeder


class SeedOPIC(ThresholdSeeder):

    def __init__(self, threshold=0, label=None, start=None, return_type="integer", s_filter=None):
        super(SeedOPIC, self).__init__(threshold=threshold, return_type=return_type, s_filter=s_filter)
        self.start = start

        if label is None:
            self._gen_name("CD-opic")
        else:
            self.name = label

    def seed(self, G):

        start = self.start
        if start is None:
            start = self.random_vertex(G)

        opic = OPIC(G)
        opic.visit(start)
        iterations = len(G.edges())

        progress = SeedProgress(G, label=self.name, edges=iterations)

        x_axis, y_axis = [], []
        for i in range(iterations):
            max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
            max_cash = opic.cash_current[max_val]

            if opic.time > 0:
                x_axis.append(max_val)
                y_axis.append(max_cash)
            opic.visit(max_val)
            progress.update()

        x_axis, y_axis = np.array(x_axis), np.array(y_axis)

        seeds = self.pick_peaks(x_axis, y_axis, G)

        if self.s_filter is not None:
            seeds = self.s_filter.filter(seeds, G)

        progress.finish()

        return seeds

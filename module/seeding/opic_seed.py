import numpy as np

from module.crawling.OPIC import OPIC
from module.seeding.threshold_seed import ThresholdSeeder


class SeedOPIC(ThresholdSeeder):

    def __init__(self, threshold, start=None, return_type="integer", s_filter=None):
        super(SeedOPIC, self).__init__(threshold=threshold, return_type=return_type)
        self.start = start
        self.s_filter = s_filter
        self.name = f'OPIC{threshold}'
        if s_filter is not None:
            self.name = f'{self.name}_{s_filter.name}_gaussian_peak{threshold}'

    def seed(self, G):
        start = self.start
        if start is None:
            start = self.random_vertex(G)

        opic = OPIC(G, 40)
        opic.visit(start)
        iterations = len(G.edges())

        seeds = []
        x_axis, y_axis = [], []
        for i in range(iterations):
            max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
            max_cash = opic.cash_current[max_val]

            if(i % 3000 == 0):
                print(f"Crawling... {(i / iterations) * 100}%")

            if opic.time > 0:
                x_axis.append(max_val)
                y_axis.append(max_cash)
            opic.visit(max_val)

        x_axis, y_axis = np.array(x_axis), np.array(y_axis)

        seeds = self.pick_peaks(x_axis, y_axis, G)

        if self.s_filter is not None:
            print(f"Filtering... {len(seeds)} seeds")
            seeds = self.s_filter.filter(seeds, G)

        return seeds


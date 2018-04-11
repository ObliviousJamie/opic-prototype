import peakutils

from module.seeding.seeder.seeder import Seeder


class ThresholdSeeder(Seeder):

    def __init__(self, threshold, return_type='string', s_filter=None, peak_filter=None):
        super(ThresholdSeeder, self).__init__(return_type)
        self.threshold = threshold
        self.s_filter = s_filter
        self.peak_filter = peak_filter

    def pick_peaks(self, x_axis, y_axis, G):
        seeds = []
        indexes = peakutils.indexes(y_axis, thres=self.threshold / max(y_axis))

        for seed in x_axis[indexes]:
            seed = self.seed_switch[self.return_type](seed)
            if seed not in seeds:
                for v in G[seed]:
                    if v in seeds:
                        break
                seeds.append(seed)

        return seeds

    def _gen_name(self, name):
        self.name = f'{name}'

        if self.peak_filter is not None:
            self.name = f'{self.name}_{self.peak_filter.name}'
        else:
            self.name = f'{self.name}_gaussian_peak{self.threshold}'

        if self.s_filter is not None:
            self.name = f'{self.name}_{self.s_filter.name}'

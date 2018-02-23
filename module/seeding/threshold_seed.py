import peakutils

from module.seeding.seed import Seeder


class ThresholdSeeder(Seeder):

    def __init__(self, threshold, return_type='string'):
        super(ThresholdSeeder, self).__init__(return_type)
        self.threshold = threshold

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

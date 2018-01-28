import numpy as np
import matplotlib.pyplot as plt
import peakutils

from module.OPIC import OPIC


class Seeder:

    def __init__(self):
        pass

    def format_string(self, index):
        return str(self.format_integer(index))

    def format_integer(self, index):
        return int(index)

    def format_float(self, index):
        pass

    def seed(self, G, start, threshold, should_plot=False, return_type="integer", print_ranks=False):

        seed_switch = {
            'integer' : self.format_integer,
            'float' : self.format_float,
            'string' : self.format_string
        }

        opic = OPIC(G, 40)
        opic.visit(start)
        iterations = len(G.edges())

        seeds = []
        x = []
        y = []
        y_axis = np.empty([1, iterations])
        x_axis = np.empty([1, iterations])
        for _ in range(iterations):
            max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
            max_cash = opic.cash_current[max_val]

            if should_plot:
                y.append(opic.cash_current[max_val])
                x.append(opic.time - 1)

            if opic.time > 0:
                y_axis.put(opic.time - 1, max_cash)
                x_axis.put(opic.time - 1, max_val)
            opic.visit(max_val)

        indexes = peakutils.indexes(y_axis[0], thres=threshold / max(y_axis[0]))
        for seed in x_axis[0][indexes]:
            seed = seed_switch[return_type](seed)
            if seed not in seeds:
                for v in G[seed]:
                    if v in seeds:
                        break
                seeds.append(seed)

        if print_ranks:
            ordered_rank = sorted(opic.cash_history, key=opic.cash_history.get, reverse=True)
            for index in ordered_rank:
                if(index in seeds):
                    print("Vertex: %s, Page Rank: %.2f" %  (index, opic.cash_history[index]))

        if should_plot:
            plt.plot(indexes, y_axis[0][indexes])
            print("Number of peaks: %s " % len(y_axis[0][indexes]))
            print("Number of seeds: %s " % len(seeds))
            # Print local maximums
            plt.plot(x, y, linewidth=0.5)
            plt.show()

        return seeds



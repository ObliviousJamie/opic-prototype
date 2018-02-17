import numpy as np
import matplotlib.pyplot as plt
import peakutils

from module.MFC import MFC
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
            'integer': self.format_integer,
            'float': self.format_float,
            'string': self.format_string
        }

        opic = OPIC(G, 40)
        opic.visit(start)
        iterations = len(G.edges())

        seeds = []
        x,y = [], []
        x_axis, y_axis = [], []
        for _ in range(iterations):
            max_val = max(opic.cash_current, key=lambda i: opic.cash_current[i])
            max_cash = opic.cash_current[max_val]

            if should_plot:
                y.append(opic.cash_current[max_val])
                x.append(opic.time - 1)

            if opic.time > 0:
                x_axis.append(max_val)
                y_axis.append(max_cash)
            opic.visit(max_val)

        x_axis, y_axis = np.array(x_axis), np.array(y_axis)

        indexes = peakutils.indexes(y_axis, thres=threshold / max(y_axis))
        for seed in x_axis[indexes]:
            seed = seed_switch[return_type](seed)
            if seed not in seeds:
                for v in G[seed]:
                    if v in seeds:
                        break
                seeds.append(seed)

        if print_ranks:
            ordered_rank = sorted(opic.cash_history, key=opic.cash_history.get, reverse=True)
            for index in ordered_rank:
                if (index in seeds):
                    print("Vertex: %s, Page Rank: %.2f" % (index, opic.cash_history[index]))

        if should_plot:
            plt.plot(indexes, y_axis[indexes])
            print("Number of peaks: %s " % len(y_axis[indexes]))
            print("Number of seeds: %s " % len(seeds))
            # Print local maximums
            plt.plot(x, y, linewidth=0.5)
            plt.show()

        return seeds

    def seed_MFC_rank(self, G, start, threshold, should_plot=False, return_type="integer", print_ranks=False):
        mfc = MFC(G, start)

        seed_switch = {
            'integer': self.format_integer,
            'float': self.format_float,
            'string': self.format_string
        }

        opic = OPIC(G, 40)
        opic.visit(start)

        seeds = []
        x, y = [], []
        x_axis, y_axis = [], []

        while not mfc.empty():
            max_val = mfc.next()
            current_cash = opic.cash_current[max_val]

            if should_plot:
                y.append(opic.cash_current[max_val])
                x.append(opic.time - 1)

            if opic.time > 0:
                x_axis.append(max_val)
                y_axis.append(current_cash)
            opic.visit(max_val)

        y_axis = np.array(y_axis)
        x_axis = np.array(x_axis)

        indexes = peakutils.indexes(y_axis, thres=threshold / max(y_axis))

        for seed in x_axis[indexes]:
            seed = seed_switch[return_type](seed)
            if seed not in seeds:
                for v in G[seed]:
                    if v in seeds:
                        break
                seeds.append(seed)

        if print_ranks:
            ordered_rank = sorted(opic.cash_history, key=opic.cash_history.get, reverse=True)
            for index in ordered_rank:
                if (index in seeds):
                    print("Vertex: %s, Page Rank: %.2f" % (index, opic.cash_history[index]))

        if should_plot:
            plt.plot(indexes, y_axis[indexes])
            print("Number of peaks: %s " % len(y_axis[indexes]))
            print("Number of seeds: %s " % len(seeds))
            # Print local maximums
            plt.plot(x, y, linewidth=0.5)
            mfc.plot()
            plt.show()

        return seeds

    def seed_MFC(self, G, start, threshold, should_plot=False, return_type="integer", min=True):
        mfc = MFC(G, start)

        seed_switch = {
            'integer': self.format_integer,
            'float': self.format_float,
            'string': self.format_string
        }

        seeds = []
        x, y = [], []

        while not mfc.empty():
            max_vertex = mfc.next()
            x.append(max_vertex)

        y_axis = []
        if min:
            for ref in mfc.y:
                if ref == 0:
                    y_axis.append(0)
                else:
                    y_axis.append(1 / ref)
        else:
            y_axis = np.array(mfc.y)

        #y_axis = np.array(mfc.y)
        x_axis = np.array(x)
        y_axis = np.array(y_axis)

        indexes = peakutils.indexes(y_axis, thres=threshold / max(y_axis))

        for seed in x_axis[indexes]:
            seed = seed_switch[return_type](seed)
            if seed not in seeds:
                for v in G[seed]:
                    if v in seeds:
                        break
                seeds.append(seed)

        if should_plot:
            ynp = np.array(y_axis)
            plt.plot(indexes, ynp[indexes])
            plt.plot(mfc.x, mfc.y)
            print("Number of peaks: %s " % len(ynp[indexes]))
            print("Number of seeds: %s " % len(seeds))
            plt.show()

        return seeds


    def mfc(self, G, start, delta=0.5):
        mfc = MFC(G, start)
        seeds = []

        communities = mfc.communities(delta=delta)
        for seed, _ in communities.items():
            if seed != -1:
                seeds.append(seed)

        return seeds

    def spreadhub(self, G, seed_limit):
        degree_seq = sorted([(degree,vertex) for vertex, degree in G.degree()], reverse=True)

        print(degree_seq)

        seeds = []
        visited = set()

        last_degree = -1
        for degree, vertex in degree_seq:
            if len(seeds) < seed_limit and vertex not in visited:
                seeds.append(vertex)
                visited.update(list(G[vertex]))
            if len(seeds) >= seed_limit and vertex not in visited:
                if degree == last_degree:
                    seeds.append(vertex)
                    visited.update(list(G[vertex]))
                else:
                    return seeds
            last_degree = degree

        print("Not enough seeds", len(seeds))
        return seeds






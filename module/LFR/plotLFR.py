from random import choice

import time

import os

from module.PPR import PPR
import subprocess
import matplotlib.pyplot as plt


class plotLFR:

    def __init__(self, method_thres_pair, save_loc=''):
        self.method_tuple_arr = method_thres_pair
        self.dir = os.path.dirname(__file__)
        self.program_prefix = os.path.join(self.dir, "nmi/onmi")
        self.community_prefix = os.path.join(self.dir, "../../data/lfr/communities/")
        self.save_loc = save_loc

    def plot(self, sizes, mixes, overlaps):

        for size in sizes:
            for mix in mixes:
                plt.title("Size: %s, Mixing factor: %s" % (size, mix))
                plt.xlabel('Fraction of overlapping nodes')
                plt.ylabel('NMI')
                plt.ylim([0, 1])

                for method, threshold in self.method_tuple_arr:
                    x, y = self.read_NMIs(method, threshold, size, mix, overlaps)
                    plt.plot(x, y, label=method)
                plt.legend()
                if self.save_loc != '':
                    now = time.strftime('M%m_D%d_min%M')
                    save = "%s/NMI_lfr_%s_%s_%s.png" % (self.save_loc, size, mix, now)
                    print("Saving plot at %s" % save)
                    plt.savefig(save)
                plt.close()

    def read_NMIs(self, method, threshold, size, mix, overlaps):
        score_arr = []
        overlap_arr = []
        for overlap in overlaps:
            nmi = self.read(method, threshold, size, mix, overlap)
            nmi = float(nmi)
            score_arr.append(nmi)
            overlap_arr.append(str(overlap))

        return overlap_arr, score_arr

    def read(self, method, threshold, size, mix, overlap):
        true_file = "%s%s_%s_%s_truth.txt" % (self.community_prefix, size, mix, overlap)
        result_file = "%s%s_%s_%s_%s_t%s_result.txt" % (self.community_prefix, size, mix, overlap, method, threshold)
        arg_string = "%s %s %s" % (self.program_prefix, true_file, result_file)

        out = subprocess.run(arg_string, check=True, shell=True, stdout=subprocess.PIPE)

        decoded_array = out.stdout \
            .decode("utf-8") \
            .replace('\t', '\n') \
            .split('\n')

        nmi = decoded_array[4]

        return nmi

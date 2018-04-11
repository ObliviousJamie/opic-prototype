import time

import os

import subprocess
from pathlib import Path

import matplotlib.pyplot as plt


class PlotNMI:

    def __init__(self, method_thres_pair, save_loc=''):
        self.method_tuple_arr = method_thres_pair
        self.dir = os.path.dirname(__file__)
        self.program_prefix = os.path.join(self.dir, "nmi/onmi")
        self.community_prefix = os.path.join(self.dir, "../../data/lfr/communities/")
        self.save_loc = save_loc

    def plot(self, sizes, mixes, overlaps):
        avg_dict = {}
        for size in sizes:
            for mix in mixes:
                plt.title("Size: %s, Mixing factor: %s" % (size, mix))
                plt.xlabel('Fraction of overlapping nodes')
                plt.ylabel('NMI')
                plt.ylim([0, 1])

                for method, threshold in self.method_tuple_arr:
                    x, y = self.read_nmis(method, threshold, size, mix, overlaps)

                    avg_dict.setdefault(method, [])
                    avg = sum(y) / len(y)
                    avg_dict[method].append(avg)

                    plt.plot(x, y, label=method)
                plt.legend()
                if self.save_loc != '':
                    now = time.strftime('M%m_D%d_min%M')
                    save = "%s/NMI_lfr_%s_%s_%s.png" % (self.save_loc, size, mix, now)
                    print("Saving plot at %s" % save)
                    plt.savefig(save)
                plt.close()

        overall = []
        for k, v in avg_dict.items():
            overall_avg = sum(v) / len(v)
            overall.append((overall_avg, k))

        jsizes = "-".join(map(str, sizes))
        jmixes = "-".join(map(str, mixes))
        jover = "-".join(map(str, overlaps))
        file = open(f"{jsizes}_{jmixes}_{jover}.txt", "w")
        for avg, name in sorted(overall):
            line = f"{name} with average NMI of {avg}"
            print(line, file=file)
        file.close()

    def read_nmis(self, method, threshold, size, mix, overlaps):
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

        nmi = 0

        results = Path(result_file)
        if not results.is_file():
            print(f"WARNING: Could not find {result_file}")
        else:
            if os.path.getsize(result_file) == 0:
                print(f"WARNING: No discovered communities in {result_file}")
            else:
                out = subprocess.run(arg_string, check=True, shell=True, stdout=subprocess.PIPE)

                decoded_array = out.stdout \
                    .decode("utf-8") \
                    .replace('\t', '\n') \
                    .split('\n')

                nmi = decoded_array[4]
                print()
                print(f"{method} with NMI: {nmi}")
                print(f"{method} with Adjusted NMI: {decoded_array[1]}")
                print()

        return nmi

import networkx as nx

from module.LFR.readLFR import ReadLFR
from module.graph.tools.samples import Samples
from module.imports.importData import ImportData


class Options:

    def __init__(self, arguments):
        self.argv = arguments
        self.options = None

    def gather_opts(self):
        options = {}
        while self.argv:
            argument = self.argv.pop(0)
            if argument[0] is '-':
                options.setdefault(argument[1], list())
                while self.argv and self.argv[0][0] is not '-':
                    data = self.argv.pop(0)
                    options[argument[1]].append(data)

        self.options = options
        return options

    @staticmethod
    def is_lfr(opts):
        if 's' in opts and 'm' in opts or 'o' in opts:
            if 'd' in opts:
                print('Cannot have LFR generated graph and supplied graph. Remove -d or -s,-m and -o.')
                exit()
            return True
        elif 'd' in opts:
            if 's' in opts or 'm' in opts or 'o' in opts:
                print('Cannot have LFR generated graph and supplied graph. Remove -d or -s,-m and -o.')
                exit()
            return False
        else:
            print('Either graph file was not specified or lfr size, mix and overlap parameters were not specified.')
            exit()

    def generate_reader(self):
        if self.options is None:
            self.gather_opts()

        if Options.is_lfr(self.options):
            sizes = self.options['s']
            mixes = self.options['m']
            reader = ReadLFR(sizes, mixes)
            if 'o' in self.options:
                reader = ReadLFR(sizes, mixes, overlapping_fractions=self.options['o'])
            return reader
        else:
            return None

    def select_seeders(self):
        samples = Samples()

        if 'c' in self.options:
            seeders = samples.threshold_sensitivity()
        else:
            seeders = samples.threshold_sensitivity()

        return seeders

    def import_real(self, need_truth=False):
        data_imports = ImportData()
        if self.options is None:
            self.gather_opts()
        if 'd' not in self.options:
            print('No data given')
            exit()

        data = self.options['d']
        graph = data_imports.text_graph(data)
        truth_dict = None

        if need_truth:
            if 't' not in self.options:
                print('No ground truth given')
                exit()
            truth = self.options['t']
            truth_dict = data_imports.ground_truth_multiline(truth)

        return graph, truth_dict





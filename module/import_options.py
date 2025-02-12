import copy

from module.imports.import_data import ImportData
from module.lfr.lfr_reader import LFRReader
from module.tools.extra.samples import Samples


class Options:

    def __init__(self, arguments, parameters="smocdtl"):
        arguments = copy.copy(arguments)
        self.argv = arguments
        self.options = None
        self.parameters = parameters

    def gather_opts(self):
        options = {}
        while self.argv:
            argument = self.argv.pop(0)
            if argument[0] is '-':
                options.setdefault(argument[1], list())
                while self.argv and self.argv[0][0] is not '-':
                    data = self.argv.pop(0)
                    options[argument[1]].append(data)

        if not options:
            self._print_help(parameters=self.parameters)
            exit()

        if 'h' in options:
            self._print_help(parameters=self.parameters)
            exit()

        self.options = options
        return options

    def generate_reader(self):
        if self.options is None:
            self.gather_opts()

        if Options.is_lfr(self.options):
            sizes = self.options['s']
            mixes = self.options['m']
            reader = LFRReader(sizes, mixes)
            if 'o' in self.options:
                reader = LFRReader(sizes, mixes, overlapping_fractions=self.options['o'])
            return reader
        else:
            return None

    def select_seeders(self):
        if self.options is None:
            self.gather_opts()

        seeders = self._find_seeder(self.options.get('c', 'all'))

        return seeders

    def import_real(self, call_location, need_truth=False):
        data_imports = ImportData(call_location)
        if self.options is None:
            self.gather_opts()
        if 'd' not in self.options:
            print('No data given')
            exit()

        data = self.options['d'][0]
        graph = data_imports.text_graph(data)
        truth_dict = None

        if need_truth:
            if 't' not in self.options:
                print('No ground truth given')
                exit()
            truth = self.options['t'][0]
            truth_dict = data_imports.ground_truth_multiline(truth)

        return graph, truth_dict

    def find_seed_list(self):
        if 'l' in self.options:
            seed_list = self.options['l'][0]
            return seed_list
        return None

    @staticmethod
    def _print_help(parameters):
        blank = '                 '

        print("Options:")
        print(f"-h{blank}Print help")

        switcher = {
            "s": f"-s{blank}Benchmark network size",
            "m": f"-m{blank}Benchmark network mixing parameter",
            "o": f"-o{blank}Benchmark network overlap percentage",
            "c": f"-c{blank}Methods to use: all mfc mfcopic opic quick alternative",
            "d": f"-d{blank}Location of real graphs in edgelist format",
            "t": f"-t{blank}Location of ground truth",
            "l": f"-l{blank}Add text file containing seed vertices",
        }

        for letter in parameters:
            instruction = switcher.get(letter, None)
            if instruction is not None:
                print(instruction)

    @staticmethod
    def is_lfr(opts):
        if 's' in opts and 'm' in opts or 'o' in opts:
            if 'd' in opts:
                print('Cannot have lfr generated network and a supplied network. Remove -d or -s,-m and -o.')
                exit()
            return True
        elif 'd' in opts:
            if 's' in opts or 'm' in opts or 'o' in opts:
                print('Cannot have lfr generated network and supplied network. Remove -d or -s,-m and -o.')
                exit()
            return False
        else:
            print('Either network file was not specified or lfr size, mix and overlap parameters were not specified.')
            exit()

    @staticmethod
    def _find_seeder(seeder_group):
        samples = Samples()
        return {
            'quick': samples.quick(),
            'alternative': samples.alternative(),
            'opic': samples.opic(),
            'mfc': samples.mfc(),
            'mfcopic': samples.mfcopic(),
            'all': samples.all()
        }.get(seeder_group[0], samples.mfcopic())

import copy

from module.LFR.readLFR import ReadLFR
from module.tools.extra.samples import Samples
from module.imports.import_data import ImportData


class Options:

    def __init__(self, arguments):
        arguments = copy.copy(arguments)
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

        if not options:
            self._print_help()
            exit()

        if 'h' in options:
            self._print_help()
            exit()

        self.options = options
        return options

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
        if self.options is None:
            self.gather_opts()

        seeders = self._find_seeder(self.options.get('c', 'mfcopic'))

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

    @staticmethod
    def _print_help():
        blank = '                 '
        print("Options:")
        print(f"-h{blank}Print help")
        print(f"-s{blank}Benchmark tools size")
        print(f"-m{blank}Benchmark tools mixing parameter")
        print(f"-o{blank}Benchmark tools overlap percentage")
        print(f"-c{blank}Methods to use: standard all mfcopic")
        print(f"-d{blank}Location of real tools in edgelist format")
        print(f"-t{blank}Location of ground truth")

    @staticmethod
    def is_lfr(opts):
        if 's' in opts and 'm' in opts or 'o' in opts:
            if 'd' in opts:
                print('Cannot have LFR generated tools and supplied tools. Remove -d or -s,-m and -o.')
                exit()
            return True
        elif 'd' in opts:
            if 's' in opts or 'm' in opts or 'o' in opts:
                print('Cannot have LFR generated tools and supplied tools. Remove -d or -s,-m and -o.')
                exit()
            return False
        else:
            print('Either tools file was not specified or lfr size, mix and overlap parameters were not specified.')
            exit()

    @staticmethod
    def _find_seeder(seeder_group):
        samples = Samples()
        return {
            'standard': samples.standard(),
            'all': samples.all(),
            'mfcopic': samples.mfcopic()
        }.get(seeder_group[0], samples.mfcopic())

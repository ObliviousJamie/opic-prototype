class plotLFR:

    def __init__(self, LFR_reader, seeder):
        self.LFR_reader = LFR_reader
        self.seeder = seeder

    def compute_communities(self):
        lfr_graphs = self.LFR_reader.read()

        for key, value in lfr_graphs.items():
            print("Key: %s Value %s" % (key, value))



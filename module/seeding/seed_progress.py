from tqdm import tqdm


class SeedProgress:

    def __init__(self, graph, label='', edges=None):
        self.graph = graph

        if edges is None:
            total = len(graph.nodes)
        else:
            total = edges

        self.pbar = tqdm(total=total, desc=f"{label} finding seeds", unit="iterations")

    def update(self, increment=1):
        self.pbar.update(increment)

    def finish(self):
        self.pbar.close()

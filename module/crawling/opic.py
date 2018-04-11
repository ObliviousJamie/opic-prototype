class OPIC:
    """Online page importance calculation

    Keeps track of page cash and page cash history of nodes in a graph.
    """

    def __init__(self, G):
        self.local_max_vertex = -1
        self.G = G
        self.cash_current = {}
        self.time = 0
        self.start_cash = 1.0

    def visit(self, node):
        if self.time == 0:
            self.cash_current[node] = 1.0

        self.time = self.time + 1
        self._distribute(node)
        self.cash_current[node] = 0

    def _distribute(self, node):
        size = len(self.G[node])

        for v in self.G[node]:
            self.cash_current[v] = self.cash_current.get(v, self.start_cash) + (
                    self.cash_current.get(node, self.start_cash) / size)

            # Update max vertex as this has the highest current page rank
            if self.cash_current[v] >= self.cash_current.get(self.local_max_vertex,
                                                             0) and self.local_max_vertex != node:
                self.local_max_vertex = v
            elif self.local_max_vertex == node:
                # Node will be set to 0 so new local max will change
                self.local_max_vertex = v

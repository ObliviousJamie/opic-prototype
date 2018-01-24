class OPIC:
    """Online page importance calculation

    Keeps track of page cash and page cash history of nodes in a graph.
    """

    def __init__(self, G, time_window):
        self.G = G
        self.cash_history = {}
        self.cash_current = {}
        self.visit_time = {}
        self.window = time_window
        self.time = 0
        self.start_cash = 1.0

    def visit(self, node):
        if(self.time == 0):
            self.cash_current[node] = 1.0

        self.time = self.time + 1

        self.__distribute(node)
        self.__update_history(node)

        self.cash_current[node] = 0

    def __update_history(self, node):
        difference = self.time - self.visit_time.get(node, 0)
        cash = self.cash_current.get(node, self.start_cash)

        if difference < self.window:
            self.cash_history[node] = self.cash_history.get(node, 1.0) * ((self.window - difference) / self.window) + \
                                      cash
        else:
            self.cash_history[node] = cash * (self.window / difference)

        self.visit_time[node] = self.time

    # TODO add virtual page
    def __distribute(self, node):
        size = len(self.G[node])

        for v in self.G[node]:
            self.cash_current[v] = self.cash_current.get(v, self.start_cash) + (self.cash_current.get(node, self.start_cash) / size)


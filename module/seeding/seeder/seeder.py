from random import choice


class Seeder:

    def __init__(self, return_type="integer"):
        self.seed_switch = {
            'integer': self.format_integer,
            'float': self.format_float,
            'string': self.format_string
        }
        self.return_type = return_type
        self.name = self.__class__.__name__
        self.threshold = 0

    def format_string(self, index):
        try:
            return str(self.format_integer(index))
        except ValueError:
            return str(index)

    def format_integer(self, index):
        return int(index)

    def format_float(self, index):
        return float(index)

    def seed(self, G):
        seed = self.random_vertex(G)
        seed = self.seed_switch[self.return_type](seed)
        return seed

    def random_vertex(self, graph):
        vertex = choice(list(graph.nodes))
        return vertex

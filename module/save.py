import os


class Save:

    def __init__(self, relative_path):
        dir = os.path.dirname(__file__)
        self.location = os.path.join(dir, relative_path)


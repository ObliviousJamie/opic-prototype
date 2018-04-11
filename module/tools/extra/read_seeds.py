
class SeedReader:

    def __init__(self, location):
        self.location = location

    def read(self):
        seeds = set()
        try:
            with open(self.location) as file:
                for line in file:
                    line = line.rstrip()
                    seed_set = line.split(" ")
                    for seed in seed_set:
                        seeds.add(seed)

            return seeds

        except Exception:
            print(f"Seed file supplied at {self.location} could not be read")
            exit()

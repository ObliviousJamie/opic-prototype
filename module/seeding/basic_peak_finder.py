class PeakFinder():

    def __init__(self, threshold):
        self.threshold = threshold
        self.last = 0
        self.name = 'nrm_peak'

    def is_peak(self, value):
        difference = value - self.last
        previous = self.last
        self.last = value

        if difference > (self.threshold * previous):
            return True

        return False


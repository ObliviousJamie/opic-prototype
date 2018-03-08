from collections import deque

from module.seeding.basic_peak_finder import PeakFinder


class WindowPeakFinder(PeakFinder):

    def __init__(self, threshold, window):
        super().__init__(threshold)
        self.window = window
        self.queue = deque(window * [0.0], window)
        self.size = 0
        self.name = f"wndw_peak{threshold}"

    def is_peak(self, value):
        sum = 0
        for item in self.queue:
            sum += item

        average = 0
        if self.size > 0:
            average =  sum  / self.size

        self.queue.appendleft(value)

        if self.size != self.window:
            self.size += 1

        difference = value - average
        if difference > (self.threshold * average):
            return True




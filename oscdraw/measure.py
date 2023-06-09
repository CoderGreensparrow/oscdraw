import time
import numpy as np


class MeasureFPS:
    """
    Calculate the FPS based on two calls of the MeasureFPS.measure() function.
    :param average: How many readings to average. Default is None, so no averaging.
    """
    def __init__(self, average: int = None):
        self.last_call = None
        self.average_amount = average
        if average:
            self.average = []

    def measure(self):
        """
        Calculate the FPS based on two calls of this function.
        :return: The Calculated FPS. -1 if unavailable.
        """
        current = time.perf_counter_ns() / 1000 / 1000
        if self.last_call is None:
            fps = -1
        else:
            fps = 1/(current - self.last_call)
            self.average.append(fps)
            if len(self.average) > self.average_amount:
                self.average.pop(0)
        self.last_call = current
        if self.average_amount and len(self.average):
            return np.average(self.average)
        return fps
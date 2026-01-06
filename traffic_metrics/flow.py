import time

class FlowEstimator:
    def __init__(self, interval_sec=60):
        self.interval = float(interval_sec)
        self.last_time = time.time()
        self.counter = 0

    def update(self, new_count):
        self.counter += new_count
        now = time.time()

        if now - self.last_time >= self.interval:
            flow = self.counter
            self.counter = 0
            self.last_time = now
            return flow

        return None

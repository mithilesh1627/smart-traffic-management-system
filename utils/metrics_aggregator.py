import time
from datetime import datetime

class MetricsAggregator:
    def __init__(self, interval_sec=60):
        self.interval_sec = interval_sec
        self.last_flush_time = time.time()
        self.reset()

    def reset(self):
        self.total_vehicle_count = 0
        self.frame_count = 0

    def update(self, vehicle_count):
        self.total_vehicle_count += vehicle_count
        self.frame_count += 1

    def should_flush(self):
        return (time.time() - self.last_flush_time) >= self.interval_sec

    def flush(self):
        avg_vehicle_count = (
            self.total_vehicle_count / self.frame_count
            if self.frame_count > 0 else 0
        )

        metrics = {
            "timestamp": datetime.utcnow(),
            "vehicle_count": int(avg_vehicle_count),
            "flow": int(avg_vehicle_count),
            "density": int(avg_vehicle_count)
        }

        self.reset()
        self.last_flush_time = time.time()
        return metrics

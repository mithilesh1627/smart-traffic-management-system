class TrafficMetricsEngine:
    def __init__(self, vehicle_counter):
        self.vehicle_counter = vehicle_counter

    def update(self, detections):
        self.vehicle_counter.update(detections)
        return {
            "vehicle_count": self.vehicle_counter.get_counts()
        }

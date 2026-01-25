import time
from datetime import datetime


class MetricsAggregator:
    def __init__(
        self,
        vehicle_counter,
        flow_estimator,
        density_calculator,
        interval_sec ,
        camera_id
    ):
        self.vehicle_counter = vehicle_counter
        self.flow_estimator = flow_estimator
        self.density_calculator = density_calculator
        self.interval_sec = interval_sec
        self.camera_id = camera_id

        self.last_flush_time = time.time()
        self.interval_flow_values = []
        self.interval_density_values = []
        self.interval_vehicle_delta = {}

    def update(self, tracked_detections):
        before = self.vehicle_counter.get_counts().copy()
        self.vehicle_counter.update(tracked_detections)
        after = self.vehicle_counter.get_counts()

        newly_counted = 0
        interval_delta = {}

        for k in after:
            delta = max(after.get(k, 0) - before.get(k, 0), 0)
            if delta > 0:
                interval_delta[k] = delta
                newly_counted += delta

        # --- Flow & Density ---
        flow = self.flow_estimator.update(newly_counted)
        density = self.density_calculator.compute(len(tracked_detections))

        if flow is not None:
            self.interval_flow_values.append(flow)

        self.interval_density_values.append(density)

        
        now = time.time()
        if now - self.last_flush_time >= self.interval_sec:
            doc = {
                "camera_id": self.camera_id,
                "timestamp": datetime.utcnow(),

                
                "vehicle_count_total": after,

                
                "vehicle_count_interval": interval_delta,

                "flow": (
                    sum(self.interval_flow_values) / len(self.interval_flow_values)
                    if self.interval_flow_values else 0
                ),
                "density": (
                    sum(self.interval_density_values) / len(self.interval_density_values)
                    if self.interval_density_values else 0
                ),
            }

            
            self.interval_flow_values.clear()
            self.interval_density_values.clear()
            self.interval_vehicle_delta.clear()

            
            self.last_flush_time += self.interval_sec

            return doc

        return None

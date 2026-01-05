class TrafficMetricsEngine:
    def __init__(self, counter, density_calc):
        self.counter = counter
        self.density_calc = density_calc

    def compute(self, detections):
        counts = self.counter.count(detections)
        total = sum(counts.values())
        density = self.density_calc.compute(total)

        return {
            "vehicle_count": counts,
            "total_vehicles": total,
            "density": density
        }



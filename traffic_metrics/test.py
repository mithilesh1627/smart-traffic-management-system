from traffic_metrics.traffic_engine import TrafficMetricsEngine
from traffic_metrics.vehicle_count import VehicleCounter
from traffic_metrics.density import DensityCalculator
from ultralytics import YOLO
detections = [
    {'class_id': 2, 'bbox': [100, 200, 300, 400], 'conf': 0.9},
    {'class_id': 5, 'bbox': [350, 220, 500, 420], 'conf': 0.8},
]
model = YOLO('yolo11n.pt')
CLASS_NAMES = model.names
engine = TrafficMetricsEngine(
    counter=VehicleCounter(CLASS_NAMES),
    density_calc=DensityCalculator(roi_area_pixels=800_000)
)

metrics = engine.compute(detections)
print(metrics)
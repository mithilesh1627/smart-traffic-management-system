
from ultralytics import YOLO
from inference.tracker_adapter import extract_tracked_detections

class YOLOTracker:
    def __init__(self, model_path="yolo11n.pt", tracker_cfg="bytetrack.yaml"):
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        self.tracker_cfg = tracker_cfg

    def track(self, frame):
        results = self.model.track(
            frame,
            tracker=self.tracker_cfg,
            persist=True,
            verbose=False
        )
        return extract_tracked_detections(results)

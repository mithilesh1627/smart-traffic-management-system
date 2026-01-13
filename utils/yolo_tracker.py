from tabnanny import verbose
from ultralytics import YOLO
from utils.config import ALLOWED_CLASSES
class YOLOTracker:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")
        self.class_names = self.model.names

    def track(self, frame):
        results = self.model.track(
            frame,
            persist=True,
            conf=0.5,
            iou=0.6,
            verbose= True
        )

        detections = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = self.class_names[cls_id]

                #  FILTER HERE
                if cls_name not in ALLOWED_CLASSES:
                    continue

                detections.append({
                    "track_id": int(box.id[0]) if box.id is not None else None,
                    "class_id": cls_id,
                    "class_name": cls_name,
                    "bbox": box.xyxy[0].tolist(),
                    "confidence": float(box.conf[0])
                })

        return detections

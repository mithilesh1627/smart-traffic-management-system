from ultralytics import YOLO
from pathlib import Path

# Load model
model = YOLO("yolo11n.pt")  
CLASS_NAMES = model.names

def run_yolo_on_image(image_path: Path):
    """
    Runs YOLO and converts results to detection dict
    """
    results = model.predict(str(image_path), verbose=False)[0]

    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf[0].cpu())
        cls = int(box.cls[0].cpu())
        detections.append({
            "class_id": cls,
            "bbox": [x1, y1, x2, y2],
            "conf": conf
        })
    return detections

from utils.config import TRAFFIC_CLASS_IDS

def extract_tracked_detections(results):
    detections = []

    for r in results:
        if r.boxes is None or r.boxes.id is None:
            continue

        boxes = r.boxes.xyxy.cpu().numpy()
        cls_ids = r.boxes.cls.cpu().numpy().astype(int)
        track_ids = r.boxes.id.cpu().numpy().astype(int)
        confs = r.boxes.conf.cpu().numpy()

        for box, cls_id, track_id, conf in zip(boxes, cls_ids, track_ids, confs):
            if cls_id not in TRAFFIC_CLASS_IDS:
                continue   #  ignore non-traffic objects

            x1, y1, x2, y2 = map(int, box)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            detections.append({
                "track_id": track_id,
                "class_id": cls_id,
                "bbox": [x1, y1, x2, y2],
                "conf": float(conf),
                "center": (cx, cy)
            })

    return detections

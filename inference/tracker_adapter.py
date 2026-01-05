def extract_tracked_detections(results):
    """
    Converts Ultralytics tracked output → unified detection schema
    """
    detections = []

    r = results[0]
    if r.boxes.id is None:
        return detections

    for box in r.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        track_id = int(box.id[0])
        class_id = int(box.cls[0])
        conf = float(box.conf[0])

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        detections.append({
            "track_id": track_id,
            "class_id": class_id,
            "bbox": [x1, y1, x2, y2],
            "conf": conf,
            "center": (cx, cy)
        })

    return detections

from yolox.tracker.byte_tracker import BYTETracker
import numpy as np

tracker = BYTETracker(frame_rate=30)  # FPS optional

def update_tracker(detections, frame):
    """
    Convert YOLO detections to tracker format and update tracker
    """
    dets_for_tracker = []
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        conf = det["conf"]
        dets_for_tracker.append([x1, y1, x2, y2, conf])
    
    tracked_objs = tracker.update(np.array(dets_for_tracker), img_info=frame.shape)
    
    # Convert to dict format
    output = []
    for t in tracked_objs:
        track_id = t.track_id
        x1, y1, x2, y2 = t.tlbr
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        output.append({"track_id": track_id, "bbox": [x1, y1, x2, y2], "center_x": cx, "center_y": cy})
    return output

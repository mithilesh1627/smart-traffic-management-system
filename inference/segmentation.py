import cv2
import numpy as np

def filter_detections_by_roi(detections, road_mask):
    """
    Only keep detections inside road region
    road_mask: binary np.array same size as image (1 = road)
    """
    filtered = []
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        # compute bbox center
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        if road_mask[cy, cx] == 1:
            filtered.append(det)
    return filtered

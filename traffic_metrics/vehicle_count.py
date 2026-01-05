from collections import defaultdict

class VehicleCounter:
    def __init__(self, class_names: dict):
        """
        class_names: {0: 'person', 2: 'car', 5: 'bus', ...}
        """
        self.class_names = class_names

    def count(self, detections):
        """
        detections: list of dicts
        [
          {'class_id': 2, 'bbox': [x1, y1, x2, y2], 'conf': 0.91},
          ...
        ]
        """
        counts = defaultdict(int)

        for det in detections:
            class_id = det["class_id"]
            class_name = self.class_names[class_id]
            counts[class_name] += 1

        return dict(counts)

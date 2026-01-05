# detection schema:

# {
#   "track_id": 12,
#   "class_id": 2,
#   "bbox": [x1, y1, x2, y2],
#   "conf": 0.91,
#   "center": (cx, cy)
# }


from collections import defaultdict

class VehicleCounter:
    def __init__(self, class_names: dict, count_line_y: int):
        """
        class_names: {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
        count_line_y: y-coordinate of counting line
        """
        self.class_names = class_names
        self.count_line_y = count_line_y

        # State
        self.track_history = defaultdict(list)
        self.counted_ids = set()
        self.counts = defaultdict(int)

    def update(self, detections):
        """
        detections: list of dicts
        [
          {
            'track_id': 12,
            'class_id': 2,
            'bbox': [x1, y1, x2, y2],
            'center': (cx, cy)
          }
        ]
        """

        for det in detections:
            track_id = det["track_id"]
            class_id = det["class_id"]
            _, cy = det["center"]

            # Update track history
            self.track_history[track_id].append(cy)

            # Skip if already counted
            if track_id in self.counted_ids:
                continue

            # Check crossing
            if len(self.track_history[track_id]) >= 2:
                prev_y = self.track_history[track_id][-2]
                curr_y = self.track_history[track_id][-1]

                if prev_y < self.count_line_y <= curr_y:
                    class_name = self.class_names[class_id]
                    self.counts[class_name] += 1
                    self.counted_ids.add(track_id)

    def get_counts(self):
        return dict(self.counts)

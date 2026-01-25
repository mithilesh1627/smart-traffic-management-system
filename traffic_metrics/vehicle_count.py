from collections import defaultdict
import time

class VehicleCounter:
    def __init__(self, class_names: dict, track_ttl_sec: int = 2):
        """
        class_names: {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
        track_ttl_sec: seconds after which inactive tracks expire
        """
        self.class_names = class_names
        self.track_ttl_sec = track_ttl_sec

        
        self.active_tracks = {}          
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
        now = time.time()
        seen_track_ids = set()

        for det in detections:
            track_id = det["track_id"]
            class_id = det["class_id"]

            seen_track_ids.add(track_id)
            self.active_tracks[track_id] = now

            
            if track_id not in self.counted_ids:
                class_name = self.class_names.get(class_id, "unknown")
                self.counts[class_name] += 1
                self.counted_ids.add(track_id)

        
        expired_tracks = [
            tid for tid, last_seen in self.active_tracks.items()
            if now - last_seen > self.track_ttl_sec
        ]

        for tid in expired_tracks:
            self.active_tracks.pop(tid, None)
            self.counted_ids.discard(tid)

    def get_counts(self):
        return dict(self.counts)

class FlowEstimator:
    def __init__(self, line_y: int):
        """
        line_y: horizontal line position (pixel)
        """
        self.line_y = line_y
        self.crossed_ids = set()

    def update(self, tracked_objects):
        """
        tracked_objects:
        [
          {'track_id': 12, 'center_y': 320},
          ...
        ]
        """
        flow_count = 0

        for obj in tracked_objects:
            tid = obj["track_id"]
            cy = obj["center_y"]

            if cy > self.line_y and tid not in self.crossed_ids:
                self.crossed_ids.add(tid)
                flow_count += 1

        return flow_count

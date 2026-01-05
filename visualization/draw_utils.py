import cv2

def draw_counting_line(frame, y):
    h, w = frame.shape[:2]
    cv2.line(frame, (0, y), (w, y), (0, 255, 255), 2)
    cv2.putText(frame, "Counting Line", (10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

def draw_tracks(frame, detections, class_names):
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        track_id = det["track_id"]
        class_name = class_names[det["class_id"]]

        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(
            frame,
            f"{class_name} ID:{track_id}",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )

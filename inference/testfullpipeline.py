import cv2
import time
from datetime import datetime
from ultralytics import YOLO
from pathlib import Path
from inference.tracker_adapter import extract_tracked_detections
from traffic_metrics.vehicle_count import VehicleCounter
from traffic_metrics.flow import FlowEstimator
from traffic_metrics.density import DensityCalculator
from visualization.draw_utils import draw_tracks, draw_counting_line
from utils.mongo import get_collection

# ---------------- CONFIG ----------------
VIDEO_SOURCE = Path(
    r"D:\2026\CV_Project\urban_traffic\data\test\Test_Video\Road_traffic_video.mp4"
)
COUNT_LINE_Y = 400
ROI_AREA_PIXELS = 800_000
CAMERA_ID = "cam_01"
MONGO_URI = "mongodb+srv://jarvis:4USyIpebzY47kZCV@ml-cluster.4ltlg.mongodb.net/?appName=ML-Cluster"

METRIC_INTERVAL_SEC = 60
# ---------------------------------------


# ---------------- MODEL -----------------
model = YOLO("yolo11n.pt")
class_names = model.names

# ---------------- METRICS ----------------
vehicle_counter = VehicleCounter(class_names, COUNT_LINE_Y)
flow_estimator = FlowEstimator(interval_sec=METRIC_INTERVAL_SEC)
density_calculator = DensityCalculator(ROI_AREA_PIXELS)

# ---------------- MONGO ------------------
metrics_collection = get_collection(MONGO_URI)

# ---------------- VIDEO ------------------
cap = cv2.VideoCapture(str(VIDEO_SOURCE))

# ---------------- AGGREGATION STATE ----------------
last_flush_time = time.time()
interval_flow_values = []
interval_density_values = []

# ----------------------------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # ---------- YOLO + ByteTrack ----------
    results = model.track(
        frame,
        tracker="bytetrack.yaml",
        persist=True,
        verbose=False
    )

    tracked_detections = extract_tracked_detections(results)

    # ---------- VEHICLE COUNT ----------
    before_counts = vehicle_counter.get_counts().copy()
    vehicle_counter.update(tracked_detections)
    after_counts = vehicle_counter.get_counts()

    newly_counted = sum(
        after_counts.get(k, 0) - before_counts.get(k, 0)
        for k in after_counts
    )

    # ---------- FLOW & DENSITY ----------
    flow = flow_estimator.update(newly_counted)
    density = density_calculator.compute(len(tracked_detections))

    # ---------- AGGREGATE ----------
    if flow is not None:
        interval_flow_values.append(flow)

    interval_density_values.append(density)

    # ---------- FLUSH EVERY 1 MIN ----------
    if time.time() - last_flush_time >= METRIC_INTERVAL_SEC:
        aggregated_doc = {
            "camera_id": CAMERA_ID,
            "timestamp": datetime.utcnow(),
            "vehicle_count": after_counts,  # cumulative counts
            "flow": (
                sum(interval_flow_values) / len(interval_flow_values)
                if interval_flow_values else 0
            ),
            "density": (
                sum(interval_density_values) / len(interval_density_values)
                if interval_density_values else 0
            )
        }

        metrics_collection.insert_one(aggregated_doc)
        print("[INFO] Metrics stored:", aggregated_doc)

        # reset window
        interval_flow_values.clear()
        interval_density_values.clear()
        last_flush_time = time.time()

    # ---------- VISUALIZATION ----------
    draw_counting_line(frame, COUNT_LINE_Y)
    draw_tracks(frame, tracked_detections, class_names)

    cv2.imshow("Smart Traffic Management", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

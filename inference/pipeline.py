import cv2

from inference.video_reader import VideoReader
from inference.yolo_tracker import YOLOTracker
from inference.metrics_aggregator import MetricsAggregator
from inference.mongo_writer import MongoWriter
from inference.mlflow_tracker import MLflowTracker

from traffic_metrics.vehicle_count import VehicleCounter
from traffic_metrics.flow import FlowEstimator
from traffic_metrics.density import DensityCalculator

from visualization.draw_utils import draw_tracks, draw_counting_line
from utils.config import (
    VIDEO_SOURCE,
    COUNT_LINE_Y,
    ROI_AREA_PIXELS,
    CAMERA_ID,
    MONGO_URI,
    METRIC_INTERVAL_SEC,
)

def main():
    video = VideoReader(VIDEO_SOURCE)
    tracker = YOLOTracker()
    mongo_writer = MongoWriter(MONGO_URI)
    mlflow_tracker = MLflowTracker(
    experiment_name="Smart_Traffic_Inference",
    camera_id=CAMERA_ID,
    model_name="yolo11n",
    metric_interval=METRIC_INTERVAL_SEC
)
    vehicle_counter = VehicleCounter(tracker.class_names, COUNT_LINE_Y)
    flow_estimator = FlowEstimator(interval_sec=METRIC_INTERVAL_SEC)
    density_calculator = DensityCalculator(ROI_AREA_PIXELS)

    aggregator = MetricsAggregator(
        vehicle_counter,
        flow_estimator,
        density_calculator,
        METRIC_INTERVAL_SEC,
        CAMERA_ID
    )

    while video.is_opened():
        ret, frame = video.read()
        if not ret:
            break

        detections = tracker.track(frame)
        doc = aggregator.update(detections)
        if doc :
            mongo_writer.write(doc)

            mlflow_tracker.log_metrics(
                flow=doc["flow"],
                density=doc["density"],
                vehicle_count=doc["vehicle_count"]
            )

        draw_counting_line(frame, COUNT_LINE_Y)
        draw_tracks(frame, detections, tracker.class_names)

        cv2.imshow("Smart Traffic Management", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    mlflow_tracker.close()


if __name__ == "__main__":
    main()

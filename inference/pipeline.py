from semver import process
from inference.video_reader import VideoReader
from inference.yolo_tracker import YOLOTracker
from inference.metrics_aggregator import MetricsAggregator
from inference.mongo_writer import MongoWriter
from inference.mlflow_tracker import MLflowTracker

from traffic_metrics.vehicle_count import VehicleCounter
from traffic_metrics.flow import FlowEstimator
from traffic_metrics.density import DensityCalculator
from visualization.video_writer import VideoWriter
from visualization.draw_utils import draw_tracks, draw_counting_line
from utils.config import (
    
    UPLOAD_PROCESSED_DIR,
    COUNT_LINE_Y,
    ROI_AREA_PIXELS,
    CAMERA_ID,
    MONGO_URI,
    METRIC_INTERVAL_SEC,
)


from pathlib import Path
import argparse
def parse_args():
    parser = argparse.ArgumentParser(description="Smart Traffic Inference")
    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Path to input traffic video"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    video = VideoReader(args.video)
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
    UPLOAD_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    video_name = Path(args.video).name
    print(f"Processing video: {video_name}")
    processed_video_path = UPLOAD_PROCESSED_DIR / f"processed_{video_name}"
    video_writer = VideoWriter(
    output_path=processed_video_path,
    fps=video.fps,
    frame_size=video.frame_size
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
        video_writer.write(frame)

    video.release()
    video_writer.release()
    mlflow_tracker.close()

if __name__ == "__main__":
    main()
    
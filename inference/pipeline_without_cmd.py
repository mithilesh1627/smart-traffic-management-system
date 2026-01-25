from pathlib import Path

from utils.video_reader import VideoReader
from utils.yolo_tracker import YOLOTracker
from utils.metrics_aggregator import MetricsAggregator
from utils.mongo_writer import MongoWriter

from traffic_metrics.vehicle_count import VehicleCounter
from traffic_metrics.flow import FlowEstimator
from traffic_metrics.density import DensityCalculator
from visualization.video_writer import VideoWriter
from visualization.draw_utils import draw_tracks

from utils.config import (
    VIDEO_SOURCE,
    UPLOAD_PROCESSED_DIR,
    ROI_AREA_PIXELS,
    CAMERA_ID,
    MONGO_URI,
    METRIC_INTERVAL_SEC,
)

# ---------------- MAIN ----------------
def main():
    video = VideoReader(VIDEO_SOURCE)
    tracker = YOLOTracker()
    mongo_writer = MongoWriter(MONGO_URI)

    vehicle_counter = VehicleCounter(tracker.class_names)
    flow_estimator = FlowEstimator(interval_sec=METRIC_INTERVAL_SEC)
    density_calculator = DensityCalculator(ROI_AREA_PIXELS)

    aggregator = MetricsAggregator(
        vehicle_counter=vehicle_counter,
        flow_estimator=flow_estimator,
        density_calculator=density_calculator,
        interval_sec=METRIC_INTERVAL_SEC,
        camera_id=CAMERA_ID
    )

    UPLOAD_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    video_name = Path(VIDEO_SOURCE).name
    processed_video_path = UPLOAD_PROCESSED_DIR / f"processed_{video_name}"

    video_writer = VideoWriter(
        output_path=processed_video_path,
        fps=video.fps,
        frame_size=video.frame_size
    )

    print(f"Processing video: {video_name}")
    try :
        while video.is_opened():
            ret, frame = video.read()
            if not ret:
                break

            detections = tracker.track(frame)
            doc = aggregator.update(detections)
            # print(f"Processed frame {video.current_frame} / {video.total_frames}", end="\r")

            print(doc)
            if doc:
                mongo_writer.write(doc)

            draw_tracks(frame, detections, tracker.class_names)
            video_writer.write(frame)
    except Exception as e:
        print(f"[ERROR] An error occurred during video processing: {e}")
    
    finally:
        video.release()
        video_writer.release()
        # mongo_writer.close()
        print(f"\nProcessed video saved to: {processed_video_path}")

if __name__ == "__main__":
    main()

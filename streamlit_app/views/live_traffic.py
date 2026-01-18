import cv2
import time
from datetime import datetime
from pathlib import Path
import sys
import streamlit as st
from ultralytics import YOLO

# ---------------- PATH FIX ----------------
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# ---------------- PROJECT IMPORTS ----------------
from utils.tracker_adapter import extract_tracked_detections
from traffic_metrics.vehicle_count import VehicleCounter
from traffic_metrics.flow import FlowEstimator
from traffic_metrics.density import DensityCalculator
from visualization.draw_utils import draw_tracks
from utils.mongo_helper import get_collection
from components.camera_utils import detect_cameras
from utils.config import (
    ROI_AREA_PIXELS,
    MONGO_URI,
    METRIC_INTERVAL_SEC
)

# ---------------- CACHE MODEL ----------------
@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")

# ---------------- MAIN VIEW ----------------
def show_live_traffic():
    if "running" not in st.session_state:
        st.session_state.running = False
    st.header(" Live Traffic Monitoring")

    # ---------- SOURCE SELECTION ----------
    source_type = st.radio(
        "Select Video Source",
        ["USB Camera", "RTSP / CCTV Stream"]
    )

    selected_source = None
    camera_id = None

    if source_type == "USB Camera":
        cameras = detect_cameras()

        if not cameras:
            st.error(" No USB cameras detected")
            return

        cam_index = st.selectbox(
            "Select Camera",
            cameras,
            format_func=lambda x: f"Camera {x}"
        )

        selected_source = cam_index
        camera_id = f"usb_{cam_index}"

    else:
        rtsp_url = st.text_input(
            "RTSP / CCTV URL",
            placeholder="rtsp://username:password@ip:port/stream"
        )

        if not rtsp_url:
            st.warning("Please enter RTSP URL")
            return

        selected_source = rtsp_url
        camera_id = "rtsp_01"

    # ---------- CONTROL BUTTONS ----------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ Start Live Inference"):
            st.session_state.running = True

    with col2:
        if st.button("⏹ Stop"):
            st.session_state.running = False

    if not st.session_state.running:
        st.info("Click **Start Live Inference** to begin")
        return

    # ---------- LOAD MODEL ----------
    model = load_model()
    class_names = model.names

    # ---------- METRICS ----------
    vehicle_counter = VehicleCounter(class_names)
    flow_estimator = FlowEstimator(interval_sec=METRIC_INTERVAL_SEC)
    density_calculator = DensityCalculator(ROI_AREA_PIXELS)

    # ---------- MONGO ----------
    metrics_collection = get_collection(MONGO_URI)

    # ---------- VIDEO CAPTURE ----------
    cap = cv2.VideoCapture(selected_source)
    if not cap.isOpened():
        st.error(" Unable to open video stream")
        st.session_state.running = False
        return

    frame_placeholder = st.empty()

    last_flush_time = time.time()
    interval_flow = []
    interval_density = []

    st.success(f" Live inference started ({camera_id})")

    # ---------- LOOP ----------
    while cap.isOpened() and st.session_state.running:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠ Stream disconnected")
            break

        results = model.track(
            frame,
            tracker="bytetrack.yaml",
            persist=True,
            verbose=False
        )

        tracked = extract_tracked_detections(results)

        before = vehicle_counter.get_counts().copy()
        vehicle_counter.update(tracked)
        after = vehicle_counter.get_counts()

        newly_counted = sum(
            after.get(k, 0) - before.get(k, 0)
            for k in after
        )

        flow = flow_estimator.update(newly_counted)
        density = density_calculator.compute(len(tracked))

        if flow is not None:
            interval_flow.append(flow)
        interval_density.append(density)

        # ---------- MONGO FLUSH ----------
        if time.time() - last_flush_time >= METRIC_INTERVAL_SEC:
            metrics_collection.insert_one({
                "camera_id": camera_id,
                "timestamp": datetime.utcnow(),
                "vehicle_count": after,
                "flow": sum(interval_flow) / len(interval_flow) if interval_flow else 0,
                "density": sum(interval_density) / len(interval_density) if interval_density else 0
            })

            interval_flow.clear()
            interval_density.clear()
            last_flush_time = time.time()

        draw_tracks(frame, tracked, class_names)

        frame_placeholder.image(
            frame,
            channels="BGR",
            caption=f"Camera: {camera_id}"
        )

    cap.release()
    st.session_state.running = False
    st.info(" Live inference stopped")

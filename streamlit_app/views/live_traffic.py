import streamlit as st
import cv2
import time
from ultralytics import YOLO
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from visualization.draw_utils import draw_tracks, draw_counting_line
from inference.tracker_adapter import extract_tracked_detections
from components.camera_utils import detect_cameras
from utils.config import COUNT_LINE_Y
@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")

def show_live_traffic():
    st.header(" Live Traffic Monitoring (Camera)")
    st.caption("Select camera → Start inference")

    # ---------- Detect Cameras ----------
    cameras = detect_cameras()

    if not cameras:
        st.error(" No camera detected")
        return

    selected_cam = st.selectbox(
        " Select Camera",
        cameras,
        format_func=lambda x: f"Camera {x}"
    )
    model = load_model()
    class_names = model.names

    start = st.button("▶ Start Camera")
    stop = st.button("⏹ Stop Camera")

    frame_placeholder = st.empty()

    if start:
        cap = cv2.VideoCapture(selected_cam)  # 0 = default webcam

        if not cap.isOpened():
            st.error(" Unable to open camera")
            return

        st.success(f"Camera {selected_cam} started")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("Camera frame not received")
                break

            # YOLO + ByteTrack
            results = model.track(
                frame,
                tracker="bytetrack.yaml",
                persist=True,
                verbose=False
            )

            tracked_detections = extract_tracked_detections(results)

            draw_counting_line(frame, COUNT_LINE_Y)
            draw_tracks(frame, tracked_detections, class_names)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

            time.sleep(0.03)  # ~30 FPS

            if stop:
                break

        cap.release()
        st.info("Camera stopped")

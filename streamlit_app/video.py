import cv2
import streamlit as st
from pathlib import Path


def stream_video(
    video_path: Path,
    frame_skip: int = 5,
    resize_width: int | None = None
):
    print("Streaming video:", video_path)
    if not video_path.exists():
        st.warning(" Video file not found")
        return

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        st.error(" Unable to open video stream")
        return

    frame_placeholder = st.empty()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Convert BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Optional resize
        if resize_width:
            h, w, _ = frame.shape
            scale = resize_width / w
            frame = cv2.resize(frame, (resize_width, int(h * scale)))

        frame_placeholder.image(
            frame,
            channels="RGB",
            use_container_width=True
        )

    cap.release()

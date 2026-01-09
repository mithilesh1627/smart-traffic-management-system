import streamlit as st
from upload_handler import save_uploaded_video
from video import stream_video
from mongo_reader import load_metrics
from charts import traffic_charts, vehicle_count_chart
import sys
from pathlib import Path
from config_streamlit import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    UPLOAD_PROCESSED_DIR
)

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from inference.run_job import run_video_inference

st.set_page_config(layout="wide", page_title="Smart Traffic AI")

st.title("🚦 Smart Traffic Video Analyzer")

# ---------------- VIDEO UPLOAD ----------------
uploaded_video = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4", "avi", "mov"]
)

if uploaded_video:
    st.success("Video uploaded successfully")

    video_path = save_uploaded_video(uploaded_video)
    
    st.video(str(video_path))

    if st.button(" Process Video"):
        with st.spinner("Processing traffic video..."):
            run_video_inference(video_path)

        st.success("Processing completed")
        # ---------------- LOAD RESULTS ----------------
        df = load_metrics(
            MONGO_URI,
            DB_NAME,
            COLLECTION_NAME
        )

        if not df.empty:
            st.subheader(" Traffic Summary")

            traffic_charts(df)
            vehicle_count_chart(df)

            st.subheader(" Processed Output")
            stream_video(
                video_path= UPLOAD_PROCESSED_DIR / f"processed_{video_path.name}",
                frame_skip=5,
                resize_width=900
            )

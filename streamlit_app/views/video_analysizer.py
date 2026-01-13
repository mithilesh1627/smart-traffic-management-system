import streamlit as st
from components.upload_handler import save_uploaded_video
from components.video import stream_video
from components.mongo_reader import load_metrics
from components.charts import traffic_charts, vehicle_count_chart
import sys
from pathlib import Path
from components.config_streamlit import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    UPLOAD_PROCESSED_DIR
)

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from components.run_job import run_video_inference

st.set_page_config(layout="wide", page_title="Smart Traffic AI")

def show_video_analyzer():
    st.title("  Traffic Video Analyzer")
    st.divider()

    uploaded_video = st.file_uploader(
        "Upload Traffic Video",
        type=["mp4", "avi", "mov"]
    )

    if not uploaded_video:
        st.info("Please upload a traffic video to begin analysis")
        return

    st.success("Video uploaded successfully")

    video_path = save_uploaded_video(uploaded_video)
    st.video(str(video_path))
    
    if st.button(" Process Video"):
        with st.spinner("Running traffic inference..."):
            run_video_inference(video_path)

        st.success("Processing completed")

        # ---------------- METRICS ----------------
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
            # st.write(UPLOAD_PROCESSED_DIR / f"processed_{video_path.name}")
            stream_video(
                video_path=UPLOAD_PROCESSED_DIR / f"processed_{video_path.name}",
                frame_skip=5,
                resize_width=900
            )

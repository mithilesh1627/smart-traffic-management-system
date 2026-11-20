import streamlit as st
from components.mongo_reader import load_metrics
from components.charts import traffic_charts, vehicle_count_chart
from components.video import stream_video
from components.config_streamlit import (
    MONGO_URI, DB_NAME, COLLECTION_NAME, UPLOAD_PROCESSED_DIR
)

def show_dashboard():
    st.title("🚦 Smart Traffic Management Dashboard")
    st.divider()

    df = load_metrics(MONGO_URI, DB_NAME, COLLECTION_NAME)

    if df is None or df.empty:
        st.warning("No traffic data available yet")
        return

    vehicle_series = df["vehicle_count_total"].apply(
    lambda x: sum(x.values()) if isinstance(x, dict) else 0
)


    col1, col2, col3, col4 = st.columns(4)
    latest_by_camera = df.sort_values('timestamp').groupby('camera_id').tail(1)
    latest_total = latest_by_camera['vehicle_count_total'].apply(lambda x: sum(x.values()) if isinstance(x, dict) else 0).sum()
    col1.metric("Latest cumulative count", int(latest_total))
    col2.metric("Average cumulative snapshot", round(vehicle_series.mean(), 2))
    col3.metric("Largest cumulative snapshot", int(vehicle_series.max()))
    col4.metric(
        "Latest Timestamp",
        df.iloc[-1]["timestamp"].strftime("%H:%M:%S")
    )

    st.divider()
    traffic_charts(df)
    vehicle_count_chart(df)

    st.divider()
    st.subheader("Processed Traffic Video")
    if st.checkbox("Show Video"):
        videos = sorted(UPLOAD_PROCESSED_DIR.glob('processed_*.mp4'), key=lambda p: p.stat().st_mtime, reverse=True)
        if not videos:
            st.info('Process a video first to see its annotated output.')
            return
        stream_video(
            videos[0],
            frame_skip=5,
            resize_width=900
        )

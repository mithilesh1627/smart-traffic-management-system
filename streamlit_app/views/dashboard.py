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
    col1.metric("Total Vehicles", int(vehicle_series.sum()))
    col2.metric("Avg Vehicles / Interval", round(vehicle_series.mean(), 2))
    col3.metric("Peak Traffic", int(vehicle_series.max()))
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
        stream_video(
            UPLOAD_PROCESSED_DIR / "processed_Road_traffic_video.mp4",
            frame_skip=5,
            resize_width=900
        )

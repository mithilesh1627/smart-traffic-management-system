import streamlit as st
from components.mongo_reader import load_metrics
from components.mlflow_reader import load_mlflow_runs
from components.charts import traffic_charts, vehicle_count_chart
from components.video import stream_video
from components.config_streamlit import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    UPLOAD_PROCESSED_DIR
)
# ---------------- LOAD DATA ----------------
df = load_metrics(
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME
)



def show_dashboard():
    st.title("🚦 Smart Traffic Management Dashboard")
    st.divider()
# ---------------- KPI METRICS ----------------
    if df.empty:
        st.warning(" No traffic data available yet")
        st.stop()
    st.subheader(" Key Traffic KPIs")

    vehicle_series = df["vehicle_count"].apply(
        lambda x: sum(x.values()) if isinstance(x, dict) else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(" Total Vehicles", int(vehicle_series.sum()))
    col2.metric(" Avg Vehicles / Frame", round(vehicle_series.mean(), 2))
    col3.metric(" Peak Traffic", int(vehicle_series.max()))
    col4.metric(" Latest Timestamp", df.iloc[-1]["timestamp"].strftime("%H:%M:%S"))

    st.markdown("---")

    # ---------------- TRAFFIC STATUS ----------------
    latest_state = df.iloc[-1].get("congestion_level", "Unknown")

    if latest_state == "High":
        st.error(" High congestion detected – traffic control recommended")
    elif latest_state == "Medium":
        st.warning(" Moderate traffic – monitor closely")
    elif latest_state == "Low":
        st.success(" Traffic flowing smoothly")
    else:
        st.info("ℹ Congestion status unavailable")

    # ---------------- CHARTS ----------------
    traffic_charts(df)
    vehicle_count_chart(df)



    # ---------------- PROCESSED VIDEO ----------------

    st.markdown("---")
    st.subheader(" Live Traffic Feed")
    if st.checkbox("Show Live Video"):
        stream_video(
            video_path=UPLOAD_PROCESSED_DIR /'processed_Road_traffic_video.mp4',
            frame_skip=5,        
            resize_width=900
        )

import streamlit as st
import mlflow
import sys
from pathlib import Path

from mongo_reader import load_metrics
from mlflow_reader import load_mlflow_runs
from charts import traffic_charts, vehicle_count_chart
from video import stream_video
from config_streamlit import (
    OUTPUT_DIR,
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
)

# ---------------- PATH SETUP ----------------
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Traffic Management",
    page_icon="🚦",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center;'>🚦 Smart Traffic Management Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# ---------------- LOAD DATA ----------------
df = load_metrics(
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME
)

if df.empty:
    st.warning(" No traffic data available yet")
    st.stop()

# ---------------- KPI METRICS ----------------
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
        video_path=OUTPUT_DIR,
        frame_skip=5,        
        resize_width=900
    )


# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Smart Traffic Management System | Computer Vision + MLOps")
st.caption("Developed by Mithilesh Chaurasiya")
import streamlit as st
import mlflow
from mongo_reader import load_metrics
from mlflow_reader import load_mlflow_runs
from config_streamlit import (VIDEO_SOURCE,MONGO_URI,DB_NAME,COLLECTION_NAME,EXPERIMENT_NAME)
from charts import traffic_charts, vehicle_count_chart, mlflow_comparison
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

st.set_page_config(layout="wide")
st.title(" Smart Traffic Management Dashboard")


df = load_metrics(
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME
)

if df.empty:
    st.warning("No traffic data available yet")
    st.stop()

# ------------------ Charts ------------------
traffic_charts(df)
vehicle_count_chart(df)


st.divider()
st.header(" Traffic Camera Feed")

st.video(VIDEO_SOURCE)
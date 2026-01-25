import streamlit as st
import pandas as pd
from datetime import datetime

from utils.mongo_helper import get_collection
from components.config_streamlit import (
    MONGO_URI,
    DB_NAME,
    AGGREGATED_COLLECTION_NAME
)


def show_hourly_dashboard():
    """
    Streamlit dashboard for hourly traffic analytics
    (Aggregated via Airflow inference_analytics DAG)
    """

    st.title("🚦 Hourly Traffic Analytics")
    st.caption("Aggregated using Airflow (1-hour time windows)")

    st.info(
        "If no data is visible on this page, it means the **Airflow inference_analytics DAG** "
        "has not produced any aggregated results."
    )

    # ---------------- MONGO CONNECTION ----------------
    col = get_collection(
        MONGO_URI,
        DB_NAME,
        AGGREGATED_COLLECTION_NAME
    )

    # ---------------- FETCH DATA ----------------
    data = list(
        col.find({}, {"_id": 0}).sort("start_time", -1)
    )

    if not data:
        st.warning("No aggregated analytics available for the last hour.")
        return

    df = pd.DataFrame(data)

    # ---------------- DATETIME FORMAT ----------------
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])

    # ---------------- SIDEBAR FILTERS ----------------
    st.subheader("🎥 Camera Filters")

    cameras = ["All"] + sorted(df["camera_id"].unique().tolist())
    selected_camera = st.selectbox("Select Camera", cameras)

    if selected_camera != "All":
        df = df[df["camera_id"] == selected_camera]

    # ---------------- KPI METRICS ----------------
    st.subheader(" Traffic KPIs")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(" Total Vehicles", int(df["total_vehicles"].sum()))
    col2.metric(" Avg Flow", round(df["avg_flow"].mean(), 2))
    col3.metric(" Avg Density", round(df["avg_density"].mean(), 2))
    col4.metric(" Peak Flow", round(df["peak_flow"].max(), 2))

    # ---------------- CONGESTION DISTRIBUTION ----------------
    st.subheader("🚦 Congestion Level Distribution")

    congestion_counts = df["congestion_level"].value_counts()
    st.bar_chart(congestion_counts)

    # ---------------- HOURLY TREND ----------------
    st.subheader(" Hourly Traffic Trend")

    trend_df = df.sort_values("start_time")

    st.line_chart(
        trend_df.set_index("start_time")[
            ["total_vehicles", "avg_flow", "avg_density"]
        ]
    )

    # ---------------- TABLE VIEW ----------------
    st.subheader(" Hourly Aggregated Data")

    display_df = df.drop(
        columns=["vehicle_count_interval"],
        errors="ignore"
    )

    st.dataframe(
        display_df.sort_values("start_time", ascending=False),
        use_container_width=True
    )

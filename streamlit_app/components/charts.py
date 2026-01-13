import streamlit as st
import pandas as pd


def traffic_charts(df):
    st.subheader("📈 Traffic Metrics Over Time")

    required_cols = {"timestamp", "flow", "density"}
    if not required_cols.issubset(df.columns):
        st.warning("Traffic metrics not available")
        return

    df_plot = (
        df[["timestamp", "flow", "density"]]
        .dropna()
        .set_index("timestamp")
    )

    st.line_chart(df_plot)


def vehicle_count_chart(df):
    st.subheader(" Vehicle Count (Latest Snapshot)")

    if "vehicle_count_total" not in df.columns:
        st.warning("Vehicle count data not available")
        return

    latest = df.iloc[-1].get("vehicle_count_total", {})

    if isinstance(latest, dict) and latest:
        st.bar_chart(latest)
    else:
        st.warning("Vehicle count data not available")
   

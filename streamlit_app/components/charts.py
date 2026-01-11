import streamlit as st

def traffic_charts(df):
    st.subheader(" Traffic Metrics")

    df_plot = df[["timestamp", "flow", "density"]].dropna()
    st.line_chart(
        df_plot.set_index("timestamp")
    )


def vehicle_count_chart(df):
    st.subheader(" Vehicle Count (Latest Snapshot)")

    latest = df.iloc[-1].get("vehicle_count", {})

    if isinstance(latest, dict) and latest:
        st.bar_chart(latest)
    else:
        st.warning("Vehicle count data not available")

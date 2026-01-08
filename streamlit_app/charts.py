import streamlit as st

def traffic_charts(df):
    st.subheader(" Traffic Metrics")

    st.line_chart(
        df.set_index("timestamp")[["flow", "density"]]
    )


def vehicle_count_chart(df):
    st.subheader(" Vehicle Count (Latest Snapshot)")

    latest = df.iloc[-1]["vehicle_count"]
    st.bar_chart(latest,)

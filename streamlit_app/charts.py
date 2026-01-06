import streamlit as st

def traffic_charts(df):
    st.subheader(" Traffic Metrics")

    st.line_chart(
        df.set_index("timestamp")[["flow", "density"]]
    )


def vehicle_count_chart(df):
    st.subheader(" Vehicle Count (Latest Snapshot)")

    latest = df.iloc[-1]["vehicle_count"]
    st.bar_chart(latest)


def mlflow_comparison(runs_df):
    st.subheader(" MLflow Experiment Comparison")

    cols = ["run_id", "metrics.flow", "metrics.density"]
    available = [c for c in cols if c in runs_df.columns]

    st.dataframe(runs_df[available])

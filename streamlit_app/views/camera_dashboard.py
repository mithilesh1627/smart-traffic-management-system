import streamlit as st
from streamlit_autorefresh import st_autorefresh
from components.mongo_reader import load_metrics
from components.charts import traffic_charts, vehicle_count_chart
from components.config_streamlit import MONGO_URI, DB_NAME, COLLECTION_NAME

def show_camera_dashboard():
    st_autorefresh(interval=60_000, key="camera_refresh")
    st.header("📊 Camera-wise Traffic Dashboard")

   
    all_df = load_metrics(MONGO_URI, DB_NAME, COLLECTION_NAME)

    if all_df is None or all_df.empty:
        st.warning("No camera data available")
        return

    
    camera_ids = sorted(all_df["camera_id"].dropna().unique().tolist())
    camera_id = st.selectbox("Select Camera", camera_ids)

   
    df = all_df[all_df["camera_id"] == camera_id]

    if df.empty:
        st.warning("No data for selected camera")
        return

    
    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Flow", round(df["flow"].mean(), 2))
    col2.metric("Avg Density", round(df["density"].mean(), 2))
    col3.metric("Records", len(df))

    st.divider()

    
    traffic_charts(df)
    vehicle_count_chart(df)

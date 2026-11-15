import streamlit as st


def show_home():

    # ================= HERO =================
    st.markdown(
        """
        <h1 style="text-align:center;">🚦 Smart Traffic Management System</h1>
        <p style="text-align:center; font-size:18px;">
        End-to-End Computer Vision + MLOps Pipeline using YOLO, Airflow, MLflow & DVC
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:gray;'>"
        "Traffic analytics and vehicle tracking system designed for heterogeneous road conditions"
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    # ================= PROBLEM =================
    st.markdown("## 📌 Problem Statement")

    st.markdown("""
Urban traffic monitoring systems often rely on **manual analysis or fragmented tools**, 
making it difficult to extract meaningful insights such as:

- Vehicle density
- Traffic congestion
- Flow estimation
- Historical trends

This project addresses these challenges by building an **automated, reproducible traffic analytics pipeline** using modern MLOps practices.
    """)

    # ================= SOLUTION =================
    st.markdown("## 💡 Solution Overview")

    st.markdown("""
The Smart Traffic Management System transforms **raw traffic videos into structured intelligence**.

It provides:

- Automated dataset validation
- YOLO-based vehicle detection and tracking
- End-to-end Airflow orchestration
- MLflow experiment tracking
- Traffic flow & density analytics
- Interactive Streamlit dashboards
    """)

    st.divider()

    # ================= KEY FEATURES =================
    st.markdown("## ⚙️ Key Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
- **Vehicle Detection** (YOLO)
- **Object Tracking with Persistent IDs**
- **Traffic Metrics** (count, flow, density)
- **Dataset Validation & Auto-labeling**
        """)

    with col2:
        st.markdown("""
- **MLflow Experiment Tracking**
- **DVC Dataset Versioning**
- **Airflow Pipeline Automation**
- **Streamlit Analytics Dashboard**
        """)

    st.divider()

    # ================= TECH STACK =================
    st.markdown("## 🛠️ Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
**Computer Vision**
- YOLO (Ultralytics)
- OpenCV
- ByteTrack Tracking
        """)

    with col2:
        st.markdown("""
**MLOps**
- Apache Airflow
- MLflow
- DVC
- Modular pipelines
        """)

    with col3:
        st.markdown("""
**Data & Visualization**
- MongoDB
- Streamlit
- Plotly
        """)

    st.divider()


    st.markdown("## 🚀 Explore the System")

    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("🎥 Live Traffic", key="home_btn_live", use_container_width=True):
            st.session_state.page = "live_traffic"
            st.rerun()

    with colB:
        if st.button("📊 Analytics Dashboard", key="home_btn_dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with colC:
        if st.button("📤 Video Analyzer", key="home_btn_video", use_container_width=True):
            st.session_state.page = "video"
            st.rerun()

    if st.button("⏱️ Hourly Traffic Dashboard", key="home_btn_hourly", use_container_width=True):
        st.session_state.page = "hourly_dashboard"
        st.rerun()
        
    st.divider()

    st.caption(
        "Built with Computer Vision & MLOps • Designed for traffic intelligence",
        text_alignment="center"
    )
    st.caption(
        "Developed by Mithilesh Chaurasiya",
        text_alignment="center"
    )
    st.caption(
        "NIT Agartala | Ex-Infosys",
        text_alignment="center"
    )

    st.caption(
        "All rights reserved © 2026",
        text_alignment="center"
    )

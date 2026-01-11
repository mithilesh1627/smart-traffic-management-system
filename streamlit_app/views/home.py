import streamlit as st

def show_home():
    # ---------------- HERO SECTION ----------------
    st.markdown(
        """
        <h1 style="text-align:center;">🚦 Smart Traffic Management System</h1>
        <p style="text-align:center; font-size:18px;">
        AI-powered traffic analytics using Computer Vision, MLOps & Airflow
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ---------------- INTRO ----------------
    st.markdown("""
    ###  About the Project
    This system automatically analyzes traffic camera footage to **detect, track, and count vehicles**.  
    It is designed as an **end-to-end production ML system**, not just a model.

    The platform focuses on:
    - Real-world traffic monitoring
    - Scalable ML pipelines
    - Automation using Airflow
    - Data-driven traffic insights
    """)

    # ---------------- TECH STACK ----------------
    st.markdown("###  Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Computer Vision**
        - YOLOv11 (Detection & Tracking)
        - OpenCV
        - FFmpeg (Video compression)
        """)

    with col2:
        st.markdown("""
        **MLOps**
        - MLflow (Experiments)
        - Airflow (Pipelines)
        - Modular inference pipeline
        """)

    with col3:
        st.markdown("""
        **Data & Visualization**
        - MongoDB (Metrics storage)
        - Streamlit (Dashboard)
        - Interactive charts
        """)

    st.divider()

    # ---------------- PIPELINE ----------------
    st.markdown("###  System Pipeline")

    st.markdown("""
    ```
    Traffic Camera Video
           ↓
    Object Detection & Tracking
           ↓
    Vehicle Counting & Metrics
           ↓
    MongoDB Storage
           ↓
    Streamlit Dashboard
    ```
    """)

    # ---------------- FEATURES ----------------
    st.markdown("###  Key Features")

    st.markdown("""
    -  Real-time traffic analytics
    -  Vehicle-wise counting (car, bus, truck, bike)
    -  Processed traffic video output
    -  Automated pipelines with Airflow
    -  Historical trend analysis
    """)

    st.divider()

    # ---------------- ACTION BUTTONS ----------------
    st.markdown("###  Get Started")

    colA, colB = st.columns(2)

    with colA:
        if st.button(" Open Traffic Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with colB:
        if st.button(" Analyze Traffic Video", use_container_width=True):
            st.session_state.page = "video"
            st.rerun()

    # ---------------- FOOTER ----------------
    st.divider()
    st.caption(
        "Built using Computer Vision & MLOps | "
        "Designed for real-world traffic analysis ",text_alignment='center'
    )
    st.caption("Developed by Mithilesh Chaurasiya",text_alignment='center')
    st.caption("© 2026 All rights reserved.",text_alignment='center')
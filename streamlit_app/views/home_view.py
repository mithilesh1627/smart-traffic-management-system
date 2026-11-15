import streamlit as st

def show_home():
    # ================= HERO =================
    st.markdown(
        """
        <h1 style="text-align:center;">🚦 Smart Traffic Management System</h1>
        <p style="text-align:center; font-size:18px; color:#555;">
        Vehicle Detection & Multi-Object Tracking Demo | YOLOv11n + ByteTrack
        </p>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "💡 **Live Demo Notice:** This cloud demo runs on **CPU with base YOLOv11n weights and in-memory tracking**. "
        "The project was trained and evaluated on the **India Driving Dataset (IDD)**, achieving **mAP@0.5 of 0.693** "
        "(see the **Results** page). No database, login, or hardware accelerator is required to test this demo."
    )

    st.divider()

    # ================= QUICK NAVIGATION =================
    st.markdown("### 🚀 Explore the Live Demo")
    st.write("Select a module below or use the sidebar navigation:")

    col_nav1, col_nav2, col_nav3 = st.columns(3)

    with col_nav1:
        st.markdown("#### 🎬 Demo Video")
        st.write("Watch the pre-processed traffic detection video (recommended clip: 0:30–1:05) with YouTube embed.")
        if st.button("▶ Watch Demo Video", key="btn_home_demo_video", use_container_width=True):
            st.session_state.page = "demo_video"
            st.rerun()

    with col_nav2:
        st.markdown("#### 📤 Upload & Analyse")
        st.write("Upload a short traffic MP4/MOV clip, run YOLO + ByteTrack tracking, and inspect class counts.")
        if st.button("🚀 Upload & Analyse Video", key="btn_home_upload", type="primary", use_container_width=True):
            st.session_state.page = "upload_analyse"
            st.rerun()

    with col_nav3:
        st.markdown("#### 📊 Evaluation Results")
        st.write("Review the verified quantitative model metrics (mAP@0.5 0.693, mAP@0.5:0.95 0.650) across vehicle classes.")
        if st.button("📈 View Results & Metrics", key="btn_home_results", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()

    st.divider()

    # ================= ARCHITECTURE DISTINCTION =================
    st.markdown("### 🏗️ Architecture: Offline Pipeline vs. Live Cloud Showcase")

    arch_col1, arch_col2 = st.columns(2)

    with arch_col1:
        st.markdown("""
        **☁️ Live Cloud Demo (Current Environment)**
        - **Inference:** Lightweight CPU inference via Ultralytics YOLOv11n.
        - **Tracking:** Real-time ByteTrack association assigning persistent IDs across frames.
        - **Zero Infrastructure Friction:** Zero MongoDB dependency, zero external API keys, zero login.
        - **Ephemeral Storage:** Video processing operates entirely in memory / temporary storage with immediate session cleanup.
        """)

    with arch_col2:
        st.markdown("""
        **⚙️ Full Offline / Training Architecture**
        - **Data Versioning:** India Driving Dataset (IDD) versioned and tracked via **DVC**.
        - **Experiment Tracking:** Hyperparameters, validation loss, and class-wise mAP tracked in **MLflow**.
        - **Pipeline Orchestration:** Automated data validation, training, and metric aggregation DAGs via **Apache Airflow**.
        - **Time-Series Analytics:** Interval vehicle counts and flow density written to **MongoDB**.
        """)

    st.divider()

    # ================= PROBLEM & SOLUTION =================
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("### 📌 Problem Statement")
        st.markdown("""
        Urban traffic surveillance systems in developing economies face distinct challenges:
        - **Heterogeneous traffic:** High mix of two-wheelers, auto-rickshaws, buses, and pedestrians.
        - **Lane indiscipline & severe occlusion:** Vehicles frequently overlap and weave without lane boundaries.
        - **Manual or fragmented monitoring:** Conventional CCTV lacks automated real-time volume and flow classification.
        """)

    with col_p2:
        st.markdown("### 💡 Computer Vision Solution")
        st.markdown("""
        This project automates traffic stream analysis into actionable metrics:
        - **YOLOv11n Object Detection:** Localizes multiple vehicle classes simultaneously.
        - **ByteTrack Association:** Preserves vehicle identities through brief occlusions using motion and appearance cues.
        - **Class-wise Flow Accounting:** Quantifies individual volume counts per vehicle type (Car, Bus, Truck, Motorbike, Person).
        """)

    st.divider()

    # ================= TECH STACK =================
    st.markdown("### 🛠️ Technology Stack")

    ts1, ts2, ts3 = st.columns(3)

    with ts1:
        st.markdown("""
        **Computer Vision**
        - YOLO (Ultralytics)
        - ByteTrack Tracking
        - OpenCV
        """)

    with ts2:
        st.markdown("""
        **MLOps Pipeline**
        - Apache Airflow (DAGs)
        - MLflow Tracking
        - DVC (Data Version Control)
        """)

    with ts3:
        st.markdown("""
        **Application & UI**
        - Streamlit Cloud
        - Plotly Interactive Charts
        - Python 3.10+
        """)

    st.divider()

    # ================= FOOTER =================
    st.caption("Developed by **Mithilesh Chaurasiya** • NIT Agartala | Ex-Infosys")
    st.caption("Smart Traffic Management System — Research & Engineering Showcase © 2026")

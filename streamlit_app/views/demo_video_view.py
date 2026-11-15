import streamlit as st

def show_demo_video():
    st.title("🎬 Processed Traffic Demo Video")
    
    st.info(
        "⏱️ **Best clip for the presentation: 0:30–1:05 (35 seconds).** "
        "Full video: 5:06. Do not play the full video in a 10-minute talk."
    )
    
    st.markdown("### 🎥 Pre-processed Detection & Tracking Demo")
    st.caption("Demonstration of YOLOv11n vehicle detection paired with ByteTrack multi-object tracking on Indian urban traffic.")

    # YouTube embed
    st.video("https://youtu.be/I4LzCnnniyE")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("▶ Open on YouTube", "https://youtu.be/I4LzCnnniyE", use_container_width=True)
    with col2:
        st.link_button("📁 Full Video on Google Drive (108 MB)", "https://drive.google.com/file/d/1xmBCdNr5SF1Etrsip_3LKA1uowlMNEeN/view", use_container_width=True)

    st.divider()

    st.markdown("### 🔍 What This Video Demonstrates")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        - **Multi-Class Vehicle Detection:** Simultaneous detection of cars, buses, trucks, motorbikes, and pedestrians.
        - **Persistent Object Tracking:** ByteTrack maintains persistent track IDs across consecutive frames, even through moderate occlusions.
        - **Real-World Urban Conditions:** Tested against challenging dense traffic, lane indiscipline, and diverse vehicle geometries from Indian road environments.
        """)
    with col_b:
        st.markdown("""
        - **Bounding Box Annotation:** Real-time visual overlay showing `[Class] ID:[TrackID] [Confidence]`.
        - **Honest Performance Characteristics:**
            - Stable tracking on forward and receding traffic.
            - Detection boxes can flicker on turning or large articulated vehicles.
            - Small or distant vehicles with heavy occlusion can be temporarily missed.
        """)

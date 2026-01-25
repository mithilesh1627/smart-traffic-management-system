import streamlit as st

from views.dashboard import show_dashboard
from views.video_analyzer import show_video_analyzer
from views.home import show_home
from views.live_traffic import show_live_traffic
from views.camera_dashboard import show_camera_dashboard
from views.hourly_dashboard import show_hourly_dashboard
st.set_page_config(
    page_title="Smart Traffic",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚦 Smart Traffic AI")
st.sidebar.caption("AI-powered traffic monitoring")

with st.sidebar:
    if st.button("Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    st.divider()
    
    if st.button("Live Traffic", use_container_width=True):
        st.session_state.page = "live_traffic"
        st.rerun()
        
    if st.button("Hourly Traffic Dashboard", use_container_width=True):
        st.session_state.page = "hourly_dashboard"
        st.rerun()

    if st.button("Camera Dashboard", use_container_width=True):
        st.session_state.page = "camera_dashboard"
        st.rerun()
        
    if st.button("Video Analyzer", use_container_width=True):
        st.session_state.page = "video"
        st.rerun()
    
    
# ---------------- ROUTER ----------------
if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "hourly_dashboard":
    show_hourly_dashboard()

elif st.session_state.page == "camera_dashboard":
    show_camera_dashboard()

elif st.session_state.page == "video":
    show_video_analyzer()

elif st.session_state.page == "live_traffic":
    show_live_traffic()

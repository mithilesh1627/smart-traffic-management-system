import streamlit as st
import sys
import os
from pathlib import Path

# Add project root and streamlit_app directory to python path
ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

st.set_page_config(
    page_title="Smart Traffic",
    layout="wide"
)

# Safe imports for views
from views.home import show_home

def safe_load_view(module_name, func_name):
    """Safely loads views that may require external dependencies like MongoDB or .env."""
    try:
        mod = __import__(f"views.{module_name}", fromlist=[func_name])
        return getattr(mod, func_name)
    except Exception as e:
        def error_view(error=e):
            st.error(f"⚠️ Unable to load {module_name}: {error}")
            st.info(
                "This page requires local infrastructure (MongoDB, .env configuration, or a connected camera). "
                "For the self-contained live demo, please run `streamlit_app/app_live.py`."
            )
        return error_view

show_dashboard = safe_load_view("dashboard", "show_dashboard")
show_video_analyzer = safe_load_view("video_analyzer", "show_video_analyzer")
show_live_traffic = safe_load_view("live_traffic", "show_live_traffic")
show_camera_dashboard = safe_load_view("camera_dashboard", "show_camera_dashboard")
show_hourly_dashboard = safe_load_view("hourly_dashboard", "show_hourly_dashboard")

if "page" not in st.session_state:
    st.session_state.page = "home"

st.sidebar.title("🚦 Smart Traffic AI")
st.sidebar.caption("AI-powered traffic monitoring")
if os.getenv("LOCAL_PANEL_DEMO") == "1":
    st.sidebar.info("Local panel demo: base YOLO11n weights. These runs do not reproduce the reported IDD validation scores.")

with st.sidebar:
    if st.button("Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    st.divider()

    if st.button("Analytics Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()

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

# Routing
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "dashboard":
    show_dashboard()
elif st.session_state.page == "hourly_dashboard":
    show_hourly_dashboard()
elif st.session_state.page == "camera_dashboard":
    show_camera_dashboard()
elif st.session_state.page == "video":
    show_video_analyzer()
elif st.session_state.page in ("live_traffic", "live"):
    show_live_traffic()
else:
    st.session_state.page = "home"
    st.rerun()

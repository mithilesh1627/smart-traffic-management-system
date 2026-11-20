import streamlit as st
import sys
import os
from pathlib import Path

# Add project root and streamlit_app directory to python path safely
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# Import live views - zero dependency on utils.config, MongoDB, Airflow, or MLflow
from views.home_view import show_home
from views.demo_video_view import show_demo_video
from views.upload_analyse_view import show_upload_analyse
from views.results_view import show_results

# Streamlit Page Configuration
st.set_page_config(
    page_title="Smart Traffic — Live Demo",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize navigation session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Sidebar Navigation
st.sidebar.title("🚦 Smart Traffic AI")
st.sidebar.caption("Computer Vision & Tracking Showcase")
st.sidebar.divider()

# Navigation buttons
pages = {
    "home": ("🏠 Home", "Overview, architecture, and live demo guide"),
    "demo_video": ("🎬 Demo Video", "Pre-processed detection & tracking video"),
    "upload_analyse": ("📤 Upload & Analyse", "Upload video clip and run YOLO + ByteTrack"),
    "results": ("📊 Results", "Verified mAP, precision, and recall metrics")
}

for page_key, (page_label, page_desc) in pages.items():
    is_active = (st.session_state.page == page_key)
    button_type = "primary" if is_active else "secondary"
    
    if st.sidebar.button(page_label, key=f"nav_{page_key}", type=button_type, use_container_width=True):
        st.session_state.page = page_key
        st.rerun()

st.sidebar.divider()

# Deployment and Environment Info
with st.sidebar.expander("ℹ️ Demo Environment", expanded=True):
    st.markdown(f"""
    - **Host:** {os.getenv('DEMO_HOST_LABEL', 'Streamlit Community Cloud')}
    - **Compute:** CPU-only inference
    - **Model:** YOLOv11n (Base weights)
    - **Tracker:** ByteTrack
    - **Storage:** In-memory (Zero DB)
    - **Auth:** No login required
    """)

st.sidebar.caption("Mithilesh Chaurasiya • 2026")

# Route to selected page
current_page = st.session_state.page

if current_page == "home":
    show_home()
elif current_page == "demo_video":
    show_demo_video()
elif current_page == "upload_analyse":
    show_upload_analyse()
elif current_page == "results":
    show_results()
else:
    st.session_state.page = "home"
    st.rerun()

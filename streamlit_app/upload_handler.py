from config_streamlit import UPLOAD_DIR

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_video(uploaded_file):
    video_path = UPLOAD_DIR / uploaded_file.name

    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return video_path

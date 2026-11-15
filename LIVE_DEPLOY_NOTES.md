# 🚦 Live Deployment Notes: Smart Traffic Management System

## 1. Deployment Overview & Cloud Settings
- **Hosting Platform:** Streamlit Community Cloud (Free tier)
- **Repository:** `mithilesh1627/smart-traffic-management-system`
- **Branch:** `live-demo`
- **Main File Path:** `streamlit_app/app_live.py`
- **Python Version:** `3.11`
- **Live URL:** [Deploy via share.streamlit.io](https://share.streamlit.io/) → `https://smart-traffic-management-system.streamlit.app/` (or generated Streamlit app URL)

---

## 2. Package & System Dependencies
### Python Packages (`requirements-live.txt` and `requirements.txt`)
All files encoded in clean UTF-8 plain text:
```text
--extra-index-url https://download.pytorch.org/whl/cpu
streamlit
ultralytics
opencv-python-headless
torch
torchvision
numpy
pandas
plotly
Pillow
```

### System Packages (`packages.txt`)
Ensures headless OpenCV and browser-ready video re-encoding are supported:
```text
libgl1
libglib2.0-0
ffmpeg
```

---

## 3. Model Weights Honest Audit
- **Model Used in Live Demo:** `yolo11n.pt` (Repo root, 5.6 MB, Ultralytics base weights).
- **Audit Findings:** Verified that `models/yolo/best.pt` does not exist locally on the machine or in git.
- **Honest Labeling in App:**
  - The live demo explicitly displays: *"Live demo runs base YOLOv11n weights. The IDD-trained model scored mAP@0.5 0.693 — see Results page."*
  - The live demo never claims to run the fine-tuned IDD weights when running `yolo11n.pt`.

---

## 4. Cold-Start Performance & CPU Inference Optimization
- **Measured Cold-Start Time:** ~25–35 seconds on Streamlit Community Cloud initialization.
- **CPU Inference Speed:**
  - Standard frame-skip parameter defaults to `2` (processing every second frame).
  - A 30-second 30 FPS video (~900 total frames, 450 processed frames) processes in ~30–45 seconds on 2 vCPUs.
  - Video writer converts to browser-compatible H.264 using `ffmpeg` when available, enabling smooth in-browser HTML5 playback with `st.video()`.

---

## 5. Scope Boundaries: What Is LIVE vs. What Is NOT Live
### ✅ What IS Live
- **Home Page:** Project overview, architecture separation, quick navigation.
- **Demo Video Page:** Pre-processed demo video embedded via YouTube (`https://youtu.be/I4LzCnnniyE`, key clip 0:30–1:05) with Google Drive fallback.
- **Upload & Analyse Page:** Video uploader (< 50 MB / < 30 sec recommended), CPU YOLOv11n + ByteTrack tracking, green bounding boxes with `[class] ID:[number] [confidence]`, unique vehicle counts by class, and downloadable annotated output.
- **Results Page:** Verified metrics table (mAP@0.5 `0.693`, mAP@0.5:0.95 `0.650`, Precision `0.597`, Recall `0.660`, class-wise breakdown).
- **Zero Login / Zero Database Friction:** In-memory execution with zero `.env` or external database requirements.

### ❌ What Is NOT Live (By Design)
- **No Real-Time Camera / CCTV:** Physical USB/RTSP streams are disabled on Streamlit Cloud (retained in codebase for local execution).
- **No MongoDB Server:** Analytics operate purely in-memory per session; no database write or connection is required.
- **No Airflow / MLflow / DVC Daemon:** Heavy orchestration and training tracking are decoupled from the live serving interface.
- **No FastAPI / DeepSORT / Production Claims:** The system honestly represents itself as an academic/research computer vision showcase.

---

## 6. Security & Secret Audit
- **DagsHub Token Check:** Found reference in `.dvc/config` line 7. No secrets are exposed or printed in the live application or deploy logs.
- **Zero Secret Footprint:** The live demo requires zero API keys, tokens, or environment variables to function.

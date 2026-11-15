import streamlit as st
import cv2
import tempfile
import os
import shutil
import subprocess
import time
from pathlib import Path
from ultralytics import YOLO
import pandas as pd
import plotly.express as px

# Target traffic classes mapped to standardized display names
TARGET_CLASSES = {
    "car": "Car",
    "bus": "Bus",
    "truck": "Truck",
    "motorcycle": "Motorbike",
    "motorbike": "Motorbike",
    "bicycle": "Bicycle",
    "person": "Person"
}

@st.cache_resource
def load_detection_model():
    """
    Load YOLO detection model.
    Checks if models/yolo/best.pt exists locally; otherwise uses base yolo11n.pt.
    """
    root_dir = Path(__file__).resolve().parents[2]
    best_pt_path = root_dir / "models" / "yolo" / "best.pt"
    base_pt_path = root_dir / "yolo11n.pt"

    if best_pt_path.is_file():
        model = YOLO(str(best_pt_path))
        model_source = "IDD-trained YOLOv11n (best.pt)"
    elif base_pt_path.is_file():
        model = YOLO(str(base_pt_path))
        model_source = "Base YOLOv11n (yolo11n.pt)"
    else:
        # Ultralytics will auto-download yolo11n.pt if not on disk
        model = YOLO("yolo11n.pt")
        model_source = "Base YOLOv11n (downloaded)"

    return model, model_source


def draw_detection_box(frame, x1, y1, x2, y2, label_text):
    """
    Draw a clean green bounding box with label text on the frame.
    """
    green_color = (0, 255, 0)
    text_color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 2

    # Draw bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), green_color, thickness)

    # Calculate text size for background pill
    (text_w, text_h), baseline = cv2.getTextSize(label_text, font, font_scale, 1)
    
    # Ensure text background doesn't overflow top of frame
    label_y1 = max(0, y1 - text_h - baseline - 4)
    label_y2 = y1
    label_x2 = min(frame.shape[1], x1 + text_w + 6)

    # Filled green label background
    cv2.rectangle(frame, (x1, label_y1), (label_x2, label_y2), green_color, -1)

    # Text in black over green background
    cv2.putText(
        frame,
        label_text,
        (x1 + 3, label_y2 - baseline - 2),
        font,
        font_scale,
        text_color,
        1,
        cv2.LINE_AA
    )


def reencode_to_browser_h264(input_path: str, output_path: str) -> bool:
    """
    Converts raw OpenCV MP4 (mp4v codec) into browser-compatible H.264 (yuv420p)
    using ffmpeg if installed.
    """
    ffmpeg_cmd = shutil.which("ffmpeg")
    if not ffmpeg_cmd:
        return False

    cmd = [
        ffmpeg_cmd,
        "-y",
        "-i", input_path,
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "24",
        output_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except Exception:
        return False


def show_upload_analyse():
    st.title("📤 Upload & Analyse Traffic Video")
    st.caption("Run YOLOv11n vehicle detection + ByteTrack tracking on CPU with zero database dependency.")

    # Honest label per B5
    st.info(
        "ℹ️ **Model Status:** Live demo runs **base YOLOv11n weights** on CPU. "
        "The IDD-trained model scored **mAP@0.5 0.693** (see **Results** page). "
        "Detection boxes can flicker on turning/large vehicles, and small or distant vehicles can be missed."
    )

    # Settings expander
    with st.expander("⚙️ Inference Configuration", expanded=False):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            conf_threshold = st.slider(
                "Confidence Threshold",
                min_value=0.15,
                max_value=0.85,
                value=0.35,
                step=0.05,
                help="Minimum confidence score to accept a detection."
            )
        with col_c2:
            frame_skip = st.select_slider(
                "Frame Skip (CPU Speedup)",
                options=[1, 2, 3, 4],
                value=2,
                help="Process every Nth frame. Skip=2 gives 2x speedup with minimal tracking loss on 30 FPS video."
            )

    uploaded_video = st.file_uploader(
        "Upload a short traffic video (MP4, MOV, or AVI — recommend < 30 sec / < 50 MB)",
        type=["mp4", "mov", "avi"]
    )

    if not uploaded_video:
        st.info("👆 Please upload a short traffic clip to begin detection and tracking.")
        return

    # Check file size
    file_size_mb = uploaded_video.size / (1024 * 1024)
    if file_size_mb > 50:
        st.warning(f"⚠️ Video size is **{file_size_mb:.1f} MB** (> 50 MB limit). Processing on CPU may take longer.")

    # Save to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_video.read())
    tfile.flush()
    input_video_path = tfile.name

    # Preview input video
    st.markdown("#### 📺 Input Video Preview")
    st.video(input_video_path)

    run_btn = st.button("🚀 Run Detection & ByteTrack Tracking", type="primary", use_container_width=True)

    if run_btn:
        progress_bar = st.progress(0.0)
        status_text = st.empty()
        error_container = st.empty()

        try:
            status_text.text("Loading YOLO model...")
            model, model_source = load_detection_model()

            cap = cv2.VideoCapture(input_video_path)
            if not cap.isOpened():
                st.error("❌ Unable to open uploaded video stream.")
                return

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if total_frames <= 0:
                total_frames = 100

            # Target output FPS adjusted for frame skip
            output_fps = max(1.0, fps / frame_skip)

            # Temporary raw output file
            raw_out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            raw_out_path = raw_out_file.name
            raw_out_file.close()

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out_writer = cv2.VideoWriter(raw_out_path, fourcc, output_fps, (width, height))

            # Tracking structures: track_id -> class_name
            unique_tracks = {}
            frame_detections_history = []
            
            frame_idx = 0
            processed_frames = 0
            start_time = time.time()

            status_text.text("Running YOLOv11n + ByteTrack inference on CPU...")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_idx += 1
                if frame_idx % frame_skip != 0:
                    continue

                processed_frames += 1

                # Ultralytics ByteTrack tracking
                results = model.track(
                    frame,
                    tracker="bytetrack.yaml",
                    persist=True,
                    conf=conf_threshold,
                    verbose=False
                )

                current_frame_counts = {"Car": 0, "Bus": 0, "Truck": 0, "Motorbike": 0, "Person": 0, "Bicycle": 0}

                if results and len(results) > 0:
                    r = results[0]
                    boxes = r.boxes

                    if boxes is not None and len(boxes) > 0:
                        xyxy = boxes.xyxy.cpu().numpy()
                        confs = boxes.conf.cpu().numpy()
                        clss = boxes.cls.cpu().numpy().astype(int)
                        track_ids = boxes.id.cpu().numpy().astype(int) if boxes.id is not None else [None] * len(clss)

                        for box, conf, cls_id, track_id in zip(xyxy, confs, clss, track_ids):
                            raw_class = model.names.get(cls_id, "")
                            std_class = TARGET_CLASSES.get(raw_class.lower(), None)

                            # Filter only recognized traffic classes
                            if not std_class:
                                continue

                            current_frame_counts[std_class] = current_frame_counts.get(std_class, 0) + 1

                            # Update persistent tracking catalogue
                            if track_id is not None:
                                unique_tracks[int(track_id)] = std_class
                                label = f"{std_class} ID:{int(track_id)} {float(conf):.2f}"
                            else:
                                label = f"{std_class} {float(conf):.2f}"

                            # Draw bounding box and label
                            x1, y1, x2, y2 = map(int, box)
                            draw_detection_box(frame, x1, y1, x2, y2, label)

                frame_detections_history.append(current_frame_counts)

                # Write annotated frame
                out_writer.write(frame)

                # Update progress
                progress = min(1.0, frame_idx / total_frames)
                progress_bar.progress(progress)
                elapsed = time.time() - start_time
                fps_processing = processed_frames / elapsed if elapsed > 0 else 0
                status_text.text(
                    f"Processing frame {frame_idx}/{total_frames} "
                    f"({fps_processing:.1f} FPS on CPU, {len(unique_tracks)} unique vehicles tracked)..."
                )

            cap.release()
            out_writer.release()

            progress_bar.progress(1.0)
            total_elapsed = time.time() - start_time
            status_text.success(
                f"✅ Processing complete in {total_elapsed:.1f}s ({processed_frames} frames processed at {processed_frames/total_elapsed:.1f} FPS)!"
            )

            # Re-encode for browser playback
            browser_out_path = raw_out_path.replace(".mp4", "_h264.mp4")
            has_h264 = reencode_to_browser_h264(raw_out_path, browser_out_path)
            final_video_path = browser_out_path if has_h264 else raw_out_path

            # ================= DISPLAY RESULTS =================
            st.divider()
            st.markdown("### 🚦 Detection & Tracking Summary")

            # Calculate class-wise counts from unique tracked vehicles
            class_counts = {"Car": 0, "Bus": 0, "Truck": 0, "Motorbike": 0, "Person": 0, "Bicycle": 0}
            for tid, cname in unique_tracks.items():
                if cname in class_counts:
                    class_counts[cname] += 1
                else:
                    class_counts[cname] = 1

            total_vehicles = len(unique_tracks)

            # KPI Metric cards
            col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
            col_m1.metric("🚗 Total Unique", total_vehicles)
            col_m2.metric("Cars", class_counts.get("Car", 0))
            col_m3.metric("Buses", class_counts.get("Bus", 0))
            col_m4.metric("Trucks", class_counts.get("Truck", 0))
            col_m5.metric("Motorbikes", class_counts.get("Motorbike", 0))
            col_m6.metric("Pedestrians", class_counts.get("Person", 0))

            # Visual breakdown chart
            chart_df = pd.DataFrame([
                {"Vehicle Class": k, "Unique Count": v}
                for k, v in class_counts.items() if v > 0
            ])

            if not chart_df.empty:
                fig = px.bar(
                    chart_df,
                    x="Vehicle Class",
                    y="Unique Count",
                    color="Vehicle Class",
                    title="Unique Tracked Objects by Class",
                    text_auto=True,
                    color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            # Display processed video
            st.markdown("### 🎬 Processed Video with Tracking Boxes")
            
            with open(final_video_path, "rb") as vf:
                video_bytes = vf.read()

            st.video(video_bytes)

            st.download_button(
                label="📥 Download Annotated Video",
                data=video_bytes,
                file_name="smart_traffic_annotated.mp4",
                mime="video/mp4",
                use_container_width=True
            )

        except Exception as ex:
            error_container.error(f"❌ An error occurred during inference: {str(ex)}")
            st.exception(ex)
        finally:
            # Clean up input temporary file
            try:
                if os.path.exists(input_video_path):
                    os.remove(input_video_path)
            except Exception:
                pass

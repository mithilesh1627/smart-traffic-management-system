import subprocess
import sys
from pathlib import Path

def run_video_inference(video_path):
    command = [
        sys.executable,
        "-m",
        "inference.pipeline", 
        "--video",
        str(video_path)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Inference failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

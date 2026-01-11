import subprocess

def run_video_inference(video_path):
    command = [
        "python",
        "-m",
        "inference.pipeline", 
        "--video",
        str(video_path)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Inference failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
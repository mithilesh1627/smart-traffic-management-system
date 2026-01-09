# visualization/video_writer.py
import cv2
from pathlib import Path

class VideoWriter:
    def __init__(self, output_path, fps, frame_size, bitrate=2_000_000):
        self.output_path = Path(output_path)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
        self.writer = cv2.VideoWriter(
            self.output_path.as_posix(),
            fourcc,
            fps,
            frame_size
        )

    def write(self, frame):
        self.writer.write(frame)

    def release(self):
        if self.writer:
            self.writer.release()

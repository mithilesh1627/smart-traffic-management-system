import cv2

class VideoReader:
    def __init__(self, video_source):
        self.cap = cv2.VideoCapture(str(video_source))

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video: {video_source}")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_size = (self.width, self.height)

    def read(self):
        return self.cap.read()

    def is_opened(self):
        return self.cap.isOpened()

    def release(self):
        self.cap.release()

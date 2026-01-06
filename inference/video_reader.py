import cv2

class VideoReader:
    def __init__(self, video_source):
        self.cap = cv2.VideoCapture(str(video_source))

    def read(self):
        return self.cap.read()

    def is_opened(self):
        return self.cap.isOpened()

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

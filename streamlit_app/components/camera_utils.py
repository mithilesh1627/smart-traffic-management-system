import cv2


def detect_cameras(max_devices: int = 5):
    """
    Detect available camera indices.
    """
    available = []

    for idx in range(max_devices):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            available.append(idx)
            cap.release()

    return available

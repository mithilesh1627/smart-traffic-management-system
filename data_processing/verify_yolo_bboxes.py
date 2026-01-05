import cv2
from pathlib import Path
from utils.config import TRAIN_IMG_DIR, TRAIN_LABL_DIR
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

CLASS_NAMES = model.names

def draw_yolo_bboxes(
    image_dir: Path,
    label_dir: Path,
    max_images: int = 10
):
    images = list(image_dir.glob("*.jpg"))[:max_images]

    for img_path in images:
        label_path = label_dir / f"{img_path.stem}.txt"

        if not label_path.exists():
            print(f"Label missing for {img_path.name}")
            continue

        image = cv2.imread(str(img_path))
        if image is None:
            print(f"Failed to read image: {img_path}")
            continue

        h, w = image.shape[:2]

        with open(label_path) as f:
            for line in f:
                cls, xc, yc, bw, bh = map(float, line.split())

                # Convert YOLO → pixel coords
                x1 = int((xc - bw / 2) * w)
                y1 = int((yc - bh / 2) * h)
                x2 = int((xc + bw / 2) * w)
                y2 = int((yc + bh / 2) * h)

                color = (0, 255, 0)
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

                label = CLASS_NAMES.get(int(cls), str(int(cls)))
                cv2.putText(
                    image,
                    label,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

        cv2.imshow("YOLO BBox Verification", image)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    draw_yolo_bboxes(
        image_dir=TRAIN_IMG_DIR,
        label_dir=TRAIN_LABL_DIR
    )

from ultralytics import YOLO
from pathlib import Path
from airflow.exceptions import AirflowSkipException
from utils.airflow_config import (
    CONF_THRES,
    MODEL_PATH,
    DATASET_DIR
)

SPLITS = ["train", "test", "valid"]

def label_split(split: str):
    img_root = DATASET_DIR / f"Processed_dataset/{split}/images"
    label_root = DATASET_DIR / f"Processed_dataset/{split}/labels"
    done_file = label_root / ".done"
    if label_root.exists() and any(label_root.glob("*.txt")):
        raise AirflowSkipException(
            f"Labels already exist for {split}. Skipping."
        )
    if done_file.exists():
        raise AirflowSkipException(
            f"Auto-labeling already completed for {split}. Skipping."
        )
    if not img_root.exists() or not any(img_root.glob("*.jpg*")):
        raise AirflowSkipException(f"No images found for {split}.")
    
    model = YOLO(MODEL_PATH, task="detect", verbose=False)

    for img_path in img_root.glob("*.jpg*"):
        results = model(img_path, conf=CONF_THRES, verbose=False)

        for r in results:
            if r.boxes is None or len(r.boxes) == 0:
                continue

            label_path = label_root / img_path.with_suffix(".txt").name
            label_path.parent.mkdir(parents=True, exist_ok=True)

            lines = []
            for box in r.boxes:
                cls = int(box.cls)
                x, y, w, h = box.xywhn[0].tolist()
                lines.append(
                    f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
                )

            with open(label_path, "w") as f:
                f.write("\n".join(lines))

            print(f"\n Label created: {label_path}")
            
    done_file.touch()

def auto_labeling():
    for split in SPLITS:
        print(f"Auto-labeling {split} split...")
        label_split(split)

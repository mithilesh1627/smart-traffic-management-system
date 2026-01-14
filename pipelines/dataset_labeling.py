from ultralytics import YOLO
from pathlib import Path
from airflow.exceptions import AirflowSkipException
from utils.airflow_config import CONF_THRES, MODEL_PATH, DATASET_DIR

SPLITS = ["train", "test", "valid"]
MAX_LOG_IMAGES = 3

# COCO → Custom class remapping
COCO_TO_CUSTOM = {
    0: 0,   # person
    1: 1,   # bicycle
    2: 2,   # car
    3: 3,   # motorbike
    5: 4,   # bus
    7: 5,   # truck
    9: 6,   # traffic light
    10: 7,  # fire hydrant
    11: 8,  # stop sign
}

def label_split(split: str):
    img_root = DATASET_DIR / f"Processed_dataset/{split}/images"
    label_root = DATASET_DIR / f"Processed_dataset/{split}/labels"
    done_file = label_root / ".done"

    if done_file.exists():
        raise AirflowSkipException(f"{split} already labeled.")

    if not img_root.exists() or not any(img_root.glob("*.jpg*")):
        raise AirflowSkipException(f"No images found for {split}.")

    label_root.mkdir(parents=True, exist_ok=True)

    model = YOLO(MODEL_PATH, task="detect", verbose=False)

    for idx, img_path in enumerate(img_root.glob("*.jpg*")):
        results = model(img_path, conf=CONF_THRES, verbose=False)

        lines = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                coco_cls = int(box.cls)

                
                if coco_cls not in COCO_TO_CUSTOM:
                    continue

                cls = COCO_TO_CUSTOM[coco_cls]
                x, y, w, h = box.xywhn[0].tolist()

                lines.append(
                    f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
                )

        if not lines:
            continue

        label_path = label_root / img_path.with_suffix(".txt").name
        label_path.write_text("\n".join(lines))

        # LOG SAMPLE LABELS TO AIRFLOW
        if idx < MAX_LOG_IMAGES:
            print(f"\n Label created: {label_path.name}")
            for line in lines[:5]:
                print("   ", line)

    done_file.touch()
    print(f" Auto-labeling completed for {split}")

def auto_labeling():
    for split in SPLITS:
        print(f"\n Auto-labeling {split} split...")
        label_split(split)

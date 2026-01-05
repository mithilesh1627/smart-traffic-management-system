from ultralytics import YOLO
from pathlib import Path
from utils.config import DATASET_DIR,CONF_THRES,MODEL_PATH,TRAIN_IMG_DIR,TRAIN_LABL_DIR
import os 
SPLITS = ['train','test','val']

model = YOLO(model='yolo11n.pt',task='detect',verbose=True)

def label_image(split):
    img_root = TRAIN_IMG_DIR
    label_root = TRAIN_LABL_DIR

    for img_path in os.listdir(img_root):
        result = model(img_path,conf=CONF_THRES,verbose=False)

        for r in result:
            if r.boxes is None or len(r.boxes)==0:
                continue

            label_path = label_root /img_path.relative_to(img_root)
            label_path = label_path.with_suffix(".txt")
            label_path.parent.mkdir(parents=True, exist_ok=True)

            lines = []
            for box in r.boxes:
                cls = int(box.cls)
                x,y,w,h = box.xywhn[0].tolist()
                lines.append(
                    f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
                )

            with open(label_path, "w") as f:
                f.write("\n".join(lines))

def auto_labeling():
    for split in SPLITS:
        print(f"Auto-labeling {split} split...")
        label_image(split)
from ultralytics import YOLO
from pathlib import Path
from utils.config import VALID_LABL_DIR,CONF_THRES,VALID_IMG_DIR

model = YOLO(model='yolo11n.pt',task='detect',verbose=True)

for u,img_path in enumerate(VALID_IMG_DIR.rglob('*.jpg')):
    results = model(img_path,conf=float(CONF_THRES))

    for r in results:
        if r.boxes is None or len(r.boxes)==0:
            continue

        label_path = VALID_LABL_DIR / img_path.relative_to(VALID_IMG_DIR)
        label_path = label_path.with_suffix(".txt")
        label_path.parent.mkdir(parents=True, exist_ok=True)

        lines = []

        for box in r.boxes:
            cls = int(box.cls)
            x,y,w,h = box.xywhn[0].tolist()
            lines.append(
                f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
            )
        
        with open(label_path,'w') as f:
            f.write('\n'.join(lines))

        if u==2:
            break
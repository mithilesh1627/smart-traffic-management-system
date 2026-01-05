import cv2
import shutil
from pathlib import Path
from tqdm import tqdm
from utils.config import RAW_IMG_DIR,TRAIN_SPLIT_METADATA,TRAIN_IMG_DIR,TRAIN_LABL_DIR


def build_train_dataset():
    
    TRAIN_IMG_DIR.mkdir(parents=True, exist_ok=True)
    TRAIN_LABL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with open(TRAIN_SPLIT_METADATA, "r") as f:
            lines = f.readlines()

        for idx, line in enumerate(tqdm(lines, desc="Processing train images")):
            rel_path = line.strip() + ".jpg"

            img_path = RAW_IMG_DIR / rel_path
            dst_path = TRAIN_IMG_DIR / img_path.name

            if not img_path.exists():
                print("Missing:", img_path)
                continue

            shutil.copy2(img_path, dst_path)

            image = cv2.imread(str(img_path))
            if image is None:
                print("Failed to read:", img_path)
                continue

    except Exception as e:
        raise RuntimeError(f"Dataset processing failed: {e}")
    

if __name__ =='__main__':
    build_train_dataset()
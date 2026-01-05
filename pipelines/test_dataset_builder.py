import cv2
import shutil
from pathlib import Path
from tqdm import tqdm
from utils.config import RAW_IMG_DIR, TEST_SPLIT_METADATA,TEST_IMG_DIR,TEST_LABL_DIR


def build_test_dataset():

    TEST_IMG_DIR.mkdir(parents=True, exist_ok=True)
    TEST_LABL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with open(TEST_SPLIT_METADATA, "r") as f:
            lines = f.readlines()

        for idx, line in enumerate(tqdm(lines, desc="Processing test images")):
            rel_path = line.strip() + ".jpg"

            img_path = RAW_IMG_DIR / rel_path
            dst_path = TEST_IMG_DIR / img_path.name

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
    
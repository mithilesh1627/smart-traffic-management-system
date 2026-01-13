import cv2
import shutil
from tqdm import tqdm
from airflow.exceptions import AirflowSkipException
from utils.airflow_config import (RAW_IMG_DIR, TEST_SPLIT_METADATA,TEST_IMG_DIR,TEST_LABL_DIR)

DONE_FILE = TEST_LABL_DIR / ".done"

def build_test_dataset():
    print("Building test dataset...")
    print(f"Using RAW_IMG_DIR: {RAW_IMG_DIR}")
    print(f"Using TEST_SPLIT_METADATA: {TEST_SPLIT_METADATA}")
    if DONE_FILE.exists():
        raise AirflowSkipException(
            "Test dataset already built (.done exists). Skipping."
        )
    else:
        TEST_IMG_DIR.mkdir(parents=True, exist_ok=True)
        TEST_LABL_DIR.mkdir(parents=True, exist_ok=True)
    processed = 0
    try:
        with open(TEST_SPLIT_METADATA, "r") as f:
            lines = f.readlines()

        for  line in tqdm(lines, desc="Processing test images"):
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
            processed += 1

        if processed == 0:
            raise RuntimeError("No test images processed")        
        DONE_FILE.touch()

    except Exception as e:
        raise RuntimeError(f"Dataset processing failed: {e}")
    
import cv2
import shutil
from airflow.exceptions import AirflowSkipException
from tqdm import tqdm
from utils.airflow_config import RAW_IMG_DIR,VAL_SPLIT_METADATA,VALID_IMG_DIR,VALID_LABL_DIR

DONE_FILE = VALID_LABL_DIR / ".done"
def build_valid_dataset():
    print("Building valid dataset...")
    print(f"Using RAW_IMG_DIR: {RAW_IMG_DIR}")
    print(f"Using VAL_SPLIT_METADATA: {VAL_SPLIT_METADATA}")
    if DONE_FILE.exists():
        raise AirflowSkipException(
            "Valid dataset already built (.done exists). Skipping."
        )
    else:
        VALID_IMG_DIR.mkdir(parents=True, exist_ok=True)
        VALID_LABL_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    try:
        with open(VAL_SPLIT_METADATA, "r") as f:
            lines = f.readlines()

        for  line in tqdm(lines, desc="Processing valid images"):
            rel_path = line.strip() + ".jpg"

            img_path = RAW_IMG_DIR / rel_path
            dst_path = VALID_IMG_DIR / img_path.name

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
            raise RuntimeError("No validation images processed")        
        DONE_FILE.touch()

    except Exception as e:
        raise RuntimeError(f"Dataset processing failed: {e}")
    
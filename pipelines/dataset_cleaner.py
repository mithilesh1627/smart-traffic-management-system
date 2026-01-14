from pathlib import Path
import logging

def keep_only_labeled_images(img_dir: Path, label_dir: Path, split: str):
    logging.info(f"Cleaning unlabeled images for {split} split")

    removed = 0
    kept = 0

    for img_path in img_dir.glob("*.jpg"):
        label_path = label_dir / f"{img_path.stem}.txt"

        if not label_path.exists():
            img_path.unlink()  # delete image
            removed += 1
        else:
            kept += 1

    logging.info(
        f"{split} split cleaned | kept={kept}, removed={removed}"
    )

    if kept == 0:
        raise RuntimeError(
            f"No labeled images left in {split} split after cleaning"
        )
from utils.airflow_config import (
    TRAIN_IMG_DIR, TRAIN_LABL_DIR,
    TEST_IMG_DIR, TEST_LABL_DIR,
    VALID_IMG_DIR, VALID_LABL_DIR,
)

def clean_dataset():
    keep_only_labeled_images(TRAIN_IMG_DIR, TRAIN_LABL_DIR, "train")
    keep_only_labeled_images(TEST_IMG_DIR, TEST_LABL_DIR, "test")
    keep_only_labeled_images(VALID_IMG_DIR, VALID_LABL_DIR, "valid")

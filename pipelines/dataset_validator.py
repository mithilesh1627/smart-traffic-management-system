from pathlib import Path
from airflow.exceptions import AirflowException
from utils.airflow_config import (
    TRAIN_IMG_DIR,
    TRAIN_LABL_DIR,
    VALID_IMG_DIR,
    VALID_LABL_DIR,
    TEST_IMG_DIR,
    TEST_LABL_DIR,
)
import cv2
def _collect_stems(dir_path: Path, suffix: str):
    if not dir_path.exists():
        return set()
    return {p.stem for p in dir_path.glob(f"*{suffix}")}

def _validate_split(
    img_dir: Path,
    label_dir: Path,
    split_name: str,
    require_labels: bool = True,
):
    images = _collect_stems(img_dir, ".jpg")
    labels = _collect_stems(label_dir, ".txt")

    if not images:
        raise AirflowException(
            f"[{split_name}] No images found in {img_dir}"
        )

    missing_labels = images - labels
    orphan_labels = labels - images

    if require_labels and missing_labels:
        raise AirflowException(
            f"""
Dataset integrity failed for {split_name} split
Missing labels: {len(missing_labels)}
Example missing: {list(missing_labels)[:5]}
"""
        )

    if orphan_labels:
        print(
            f"[WARN] {split_name}: {len(orphan_labels)} orphan labels found"
        )

    print(
        f"[OK] {split_name} split validated | "
        f"images={len(images)} labels={len(labels)}"
    )

def validate_structure_only():
    """
    Use BEFORE auto-labeling
    """
    print("Validating dataset structure (no label requirement)...")

    for name, img_dir in {
        "train": TRAIN_IMG_DIR,
        "val": VALID_IMG_DIR,
        "test": TEST_IMG_DIR,
    }.items():
        if not img_dir.exists():
            raise AirflowException(
                f"{name} image directory missing: {img_dir}"
            )
        if not any(img_dir.iterdir()):
            raise AirflowException(
                f"{name} image directory empty: {img_dir}"
            )

    print("Dataset structure validation passed")


def validate_labels_required():
    """
    Use AFTER auto-labeling
    """
    print("Validating dataset labels (strict)...")

    _validate_split(TRAIN_IMG_DIR, TRAIN_LABL_DIR, "train", require_labels=True)
    _validate_split(VALID_IMG_DIR, VALID_LABL_DIR, "valid", require_labels=True)
    _validate_split(TEST_IMG_DIR, TEST_LABL_DIR, "test", require_labels=True)

    print("All dataset splits passed label validation")

def validate_images(images_dir: Path, labels_dir: Path, delete_corrupt=True):
    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)

    removed = 0

    for img_path in images_dir.glob("*.*"):
        label_path = labels_dir / f"{img_path.stem}.txt"

        # Skip if label missing
        if not label_path.exists():
            img_path.unlink(missing_ok=True)
            continue

        # Try loading image
        img = cv2.imread(str(img_path))
        if img is None:
            print(f" Corrupt image: {img_path}")
            removed += 1

            if delete_corrupt:
                img_path.unlink(missing_ok=True)
                label_path.unlink(missing_ok=True)

    print(f" Dataset validation complete | Removed {removed} corrupt images")

def validate_images_train_valid():
    validate_images(TRAIN_IMG_DIR, TRAIN_LABL_DIR)
    validate_images(VALID_IMG_DIR, VALID_LABL_DIR)
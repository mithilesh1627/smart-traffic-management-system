import os
from pathlib import Path
from airflow.models import Variable


PROJECT_ROOT = Path(
    Variable.get(
        "PROJECT_ROOT",
        "/mnt/d/2026/CV_Project/smart-traffic-management-system"
    )
)

DATASET_DIR = Path(
    Variable.get(
        "DATASET_DIR",
        str(PROJECT_ROOT / "IDD_Dataset")
    )
)

RAW_IMG_DIR = DATASET_DIR / "JPEGImages"

# Metadata
TRAIN_SPLIT_METADATA = DATASET_DIR / "train.txt"
VAL_SPLIT_METADATA   = DATASET_DIR / "val.txt"
TEST_SPLIT_METADATA  = DATASET_DIR / "test.txt"

# Processed datasets
TRAIN_IMG_DIR = DATASET_DIR / "Processed_dataset/train/images"
TRAIN_LABL_DIR = DATASET_DIR / "Processed_dataset/train/labels"
TEST_IMG_DIR = DATASET_DIR / "Processed_dataset/test/images"
TEST_LABL_DIR = DATASET_DIR / "Processed_dataset/test/labels"

VALID_IMG_DIR = DATASET_DIR / "Processed_dataset/valid/images"
VALID_LABL_DIR = DATASET_DIR / "Processed_dataset/valid/labels"
CONF_THRES = 0.8
MODEL_PATH = PROJECT_ROOT / "yolo11n.pt"
UPLOAD_DIR = PROJECT_ROOT / "user_upload_data"/ "uploads"
UPLOAD_PROCESSED_DIR = PROJECT_ROOT / "user_upload_data"/ "outputs"

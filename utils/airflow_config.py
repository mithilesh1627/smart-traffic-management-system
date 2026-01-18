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
PROCESSED_DATASET = DATASET_DIR / "Processed_dataset"

TRAIN_IMG_DIR = PROCESSED_DATASET/"train/images"
TRAIN_LABL_DIR = PROCESSED_DATASET /"train/labels"

TEST_IMG_DIR = PROCESSED_DATASET / "test/images"
TEST_LABL_DIR = PROCESSED_DATASET / "test/labels"

VALID_IMG_DIR = PROCESSED_DATASET / "valid/images"
VALID_LABL_DIR = PROCESSED_DATASET / "valid/labels"
CONF_THRES = 0.8
MODEL_PATH = PROJECT_ROOT / "yolo11n.pt"
UPLOAD_DIR = PROJECT_ROOT / "user_upload_data"/ "uploads"
UPLOAD_PROCESSED_DIR = PROJECT_ROOT / "user_upload_data"/ "outputs"
YOLO_RUNS_DIR = PROJECT_ROOT / "yolo_runs"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"

# MLflow
MLFLOW_TRACKING_URI="https://dagshub.com/mithilesh1627/smart-traffic-management-system.mlflow"
MLFLOW_EXPERIMENT_NAME="YOLO_Traffic_Training"
TRAINING_REGISTRY = PROJECT_ROOT / "artifacts" / "training_registry"
TRAINING_REGISTRY.mkdir(parents=True, exist_ok=True)
output_path = YOLO_RUNS_DIR /"traffic_yolo"/ "training_output.json"
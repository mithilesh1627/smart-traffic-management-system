from pathlib import Path
import os
from dotenv import load_dotenv
import os

load_dotenv()
# Base paths
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT"))
DATASET_DIR = Path(os.getenv("DATASET_DIR"))
RAW_IMG_DIR = Path(os.getenv("RAW_IMG_DIR"))


#Image and Label Dataset
TRAIN_IMG_DIR = DATASET_DIR / "Processed_dataset" / "train" / "images"
TRAIN_LABL_DIR = DATASET_DIR / "Processed_dataset" / "train" / "labels"

TEST_IMG_DIR = DATASET_DIR / "Processed_dataset" / "test" / "images"
TEST_LABL_DIR = DATASET_DIR / "Processed_dataset" / "test" / "labels"

VALID_IMG_DIR = DATASET_DIR / "Processed_dataset" / "valid" / "images"
VALID_LABL_DIR = DATASET_DIR / "Processed_dataset" / "valid" / "labels"

# Metadata paths
TRAIN_SPLIT_METADATA = PROJECT_ROOT / os.getenv("TRAIN_SPLIT_METADATA")
VAL_SPLIT_METADATA   = PROJECT_ROOT / os.getenv("VAL_SPLIT_METADATA")
TEST_SPLIT_METADATA  = PROJECT_ROOT / os.getenv("TEST_SPLIT_METADATA")


MODEL_PATH = os.getenv("MODEL_PATH")
CONF_THRES = os.getenv("CONF_THRES")

# Safety checks
for name, path in {
    "PROJECT_ROOT": PROJECT_ROOT,
    "DATASET_DIR": DATASET_DIR,
    "RAW_IMG_DIR": RAW_IMG_DIR,
    "TEST_SPLIT_METADATA": TEST_SPLIT_METADATA,
}.items():
    if path is None:
        raise ValueError(f"{name} is not set in .env")
    
VIDEO_SOURCE = Path(os.getenv('VIDEO_SOURCE'))
COUNT_LINE_Y = os.getenv('COUNT_LINE_Y')
ROI_AREA_PIXELS = os.getenv('ROI_AREA_PIXELS')
CAMERA_ID = os.getenv('CAMERA_ID')
MONGO_URI = os.getenv('MONGO_URI')
METRIC_INTERVAL_SEC = os.getenv('METRIC_INTERVAL_SEC')
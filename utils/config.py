from pathlib import Path
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
COUNT_LINE_Y = int(os.getenv('COUNT_LINE_Y'))
ROI_AREA_PIXELS = float(os.getenv('ROI_AREA_PIXELS'))
CAMERA_ID = os.getenv('CAMERA_ID')
MONGO_URI = os.getenv('MONGO_URI')
INFERENCE_COLLECTION_NAME = os.getenv('INFERENCE_COLLECTION_NAME','inference_results')
METRIC_INTERVAL_SEC = float(os.getenv('METRIC_INTERVAL_SEC',2))
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv(key='COLLECTION_NAME')
UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR'))
UPLOAD_PROCESSED_DIR = Path(os.getenv('UPLOAD_PROCESSED_DIR'))
TRAFFIC_CLASS_IDS = {0,1,2,3,5,6,7,9,10,11,12}  #  class IDs for traffic-related objects
ALLOWED_CLASSES = {
    "car",
    "truck",
    "bus",
    "motorcycle",
    "bicycle"
}
AGGREGATED_COLLECTION_NAME = os.getenv('AGGREGATED_COLLECTION_NAME','traffic_analytics_hourly')
# DAGsHub
DVC_REMOTE_NAME=os.getenv("DVC_REMOTE_NAME")
DVC_REMOTE_URL=os.getenv("DVC_REMOTE_URL")
DAGSHUB_USERNAME=os.getenv("DAGSHUB_USERNAME")
DAGSHUB_TOKEN=os.getenv("DAGSHUB_TOKEN")
# MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME")
AGGREGATED_COLLECTION_NAME = os.getenv("AGGREGATED_COLLECTION_NAME","aggregated_metrics")
# YOLO_TRAINED_MODEL
TRAINED_MODEL=PROJECT_ROOT /"models" / "yolo" / "best.pt"
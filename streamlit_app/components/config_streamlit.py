from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv(key='COLLECTION_NAME')
MLFLOW_TRACKING_URI  = os.getenv('MLFLOW_TRACKING_URI')
EXPERIMENT_NAME  = os.getenv('EXPERIMENT_NAME')
MONGO_URI = os.getenv('MONGO_URI')
VIDEO_SOURCE = Path(os.getenv('VIDEO_SOURCE'))
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR'))
UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR'))
UPLOAD_PROCESSED_DIR = Path(os.getenv('UPLOAD_PROCESSED_DIR'))
AGGREGATED_COLLECTION_NAME = os.getenv('AGGREGATED_COLLECTION_NAME')
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]

DB_NAME = os.getenv('DB_NAME', 'traffic_database')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'traffic_metrics')
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', '')
EXPERIMENT_NAME = os.getenv('EXPERIMENT_NAME', 'traffic_detection')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')

VIDEO_SOURCE_RAW = os.getenv('VIDEO_SOURCE')
VIDEO_SOURCE = Path(VIDEO_SOURCE_RAW) if VIDEO_SOURCE_RAW else ROOT_DIR / 'videos' / 'traffic_sample.mp4'

OUTPUT_DIR_RAW = os.getenv('OUTPUT_DIR')
OUTPUT_DIR = Path(OUTPUT_DIR_RAW) if OUTPUT_DIR_RAW else ROOT_DIR / 'output'

UPLOAD_DIR_RAW = os.getenv('UPLOAD_DIR')
UPLOAD_DIR = Path(UPLOAD_DIR_RAW) if UPLOAD_DIR_RAW else ROOT_DIR / 'user_upload_data'

UPLOAD_PROCESSED_DIR_RAW = os.getenv('UPLOAD_PROCESSED_DIR')
UPLOAD_PROCESSED_DIR = Path(UPLOAD_PROCESSED_DIR_RAW) if UPLOAD_PROCESSED_DIR_RAW else ROOT_DIR / 'user_upload_data' / 'processed'

AGGREGATED_COLLECTION_NAME = os.getenv('AGGREGATED_COLLECTION_NAME', 'traffic_analytics_hourly')

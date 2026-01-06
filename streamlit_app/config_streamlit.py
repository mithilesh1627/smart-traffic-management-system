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
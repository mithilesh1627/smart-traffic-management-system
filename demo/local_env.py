"""Explicit, isolated configuration for the panel demo; no credentials required."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.local-demo'

def configure():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    values = {
        'PROJECT_ROOT': str(ROOT), 'DATASET_DIR': str(ROOT / 'IDD_Dataset'),
        'RAW_IMG_DIR': str(ROOT / 'IDD_Dataset'),
        'TRAIN_SPLIT_METADATA': 'train_metadata.json',
        'VAL_SPLIT_METADATA': 'val_metadata.json', 'TEST_SPLIT_METADATA': 'test_metadata.json',
        'VIDEO_SOURCE': str(STATE / 'panel_sample.mp4'),
        'MODEL_PATH': str(ROOT / 'yolo11n.pt'), 'TRAINED_MODEL': str(ROOT / 'yolo11n.pt'),
        'CONF_THRES': '0.5', 'COUNT_LINE_Y': '300', 'ROI_AREA_PIXELS': '230400',
        'CAMERA_ID': 'panel_video', 'MONGO_URI': 'mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=3000',
        'DB_NAME': 'traffic_system', 'COLLECTION_NAME': 'metrics',
        'INFERENCE_COLLECTION_NAME': 'metrics', 'AGGREGATED_COLLECTION_NAME': 'panel_hourly',
        'METRIC_INTERVAL_SEC': '2', 'UPLOAD_DIR': str(STATE / 'uploads'),
        'UPLOAD_PROCESSED_DIR': str(STATE / 'processed'),
        'MLFLOW_TRACKING_URI': 'http://127.0.0.1:5000',
        'MLFLOW_EXPERIMENT_NAME': 'Local_Panel_Demo',
        'LOCAL_PANEL_DEMO': '1', 'DEMO_HOST_LABEL': 'Local Windows computer',
        'YOLO_CONFIG_DIR': str(STATE / 'yolo'),
        'PYTHONIOENCODING': 'utf-8',
    }
    os.environ.update(values)
    os.environ['PATH'] = str(STATE / 'bin') + os.pathsep + os.environ.get('PATH', '')
    for folder in ['uploads','processed','logs','data','bin','yolo']:
        (STATE / folder).mkdir(parents=True, exist_ok=True)
    os.chdir(ROOT)
    return values

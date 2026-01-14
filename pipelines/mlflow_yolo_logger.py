import mlflow
import pandas as pd
from pathlib import Path
from utils.airflow_config import YOLO_RUN_DIR,DATASET_DIR
from pipelines.mlflow_dvc_logger import log_dvc_metadata
def log_yolo_model():
    if not YOLO_RUN_DIR.exists():
        raise FileNotFoundError("YOLO training output not found")

    weights_dir = YOLO_RUN_DIR / "weights"
    results_csv = YOLO_RUN_DIR / "results.csv"
    args_yaml = YOLO_RUN_DIR / "args.yaml"

    best_model = weights_dir / "best.pt"

    if not best_model.exists():
        raise FileNotFoundError("best.pt not found")

    mlflow.set_experiment("Smart-Traffic-YOLO")

    with mlflow.start_run(run_name="yolo_training_v1"):

        log_dvc_metadata(DATASET_DIR)

        # 🔹 Training params
        mlflow.log_param("epochs", 50)
        mlflow.log_param("imgsz", 640)
        mlflow.log_param("batch", 16)

        # 🔹 Metrics
        if results_csv.exists():
            df = pd.read_csv(results_csv)
            last = df.iloc[-1]

            mlflow.log_metrics({
                "precision": float(last["metrics/precision(B)"]),
                "recall": float(last["metrics/recall(B)"]),
                "map50": float(last["metrics/mAP50(B)"]),
                "map5095": float(last["metrics/mAP50-95(B)"]),
            })

        #  Model artifact
        mlflow.log_artifact(str(best_model), artifact_path="model")

        #  Config artifacts
        mlflow.log_artifact(str(args_yaml), artifact_path="config")

        print(" YOLO model + DVC lineage logged")
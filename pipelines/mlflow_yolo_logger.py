import json
import mlflow
from pathlib import Path
from utils.airflow_config import MLRUNS_DIR
from pipelines.training_fingerprint import get_git_commit_hash


def log_yolo_to_mlflow(training_output_path: str):

    mlflow.set_tracking_uri(f"file://{MLRUNS_DIR}")
    mlflow.set_experiment("Smart-Traffic-YOLO")

    with open(training_output_path) as f:
        data = json.load(f)

    with mlflow.start_run(run_name=data["training_name"]):

        mlflow.log_params(data["params"])

        for m in data["metrics"]:
            step = m["epoch"]
            mlflow.log_metric("precision", m["precision"], step=step)
            mlflow.log_metric("recall", m["recall"], step=step)
            mlflow.log_metric("mAP50", m["mAP50"], step=step)
            mlflow.log_metric("mAP50_95", m["mAP50_95"], step=step)

        mlflow.log_artifact(data["weights_path"])

        mlflow.set_tag("training_signature", data["signature"])
        mlflow.set_tag("git_commit", get_git_commit_hash())
        mlflow.set_tag("pipeline", "airflow")

        print("MLflow logging completed")

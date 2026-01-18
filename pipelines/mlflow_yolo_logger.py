import json
from pathlib import Path
import mlflow
import os
from dotenv import load_dotenv
from pipelines.mlflow_dedup import mlflow_run_exists
from utils.config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    DVC_REMOTE_NAME,
    DVC_REMOTE_URL,
    DAGSHUB_USERNAME,
    DAGSHUB_TOKEN
)
from airflow.exceptions import AirflowSkipException


def log_yolo_to_mlflow(training_output_path: str):
    """
    Logs:
    - YOLO training params
    - epoch metrics
    - best.pt weights
    - git commit
    - DVC metadata
    - dataset version
    """
    print("Logging YOLO training artifacts to MLflow...")
    print(f"Training output path: {training_output_path}")
    if training_output_path is None:
             raise AirflowSkipException("No training output to log")
    

    os.environ["MLFLOW_TRACKING_USERNAME"] = DAGSHUB_USERNAME
    os.environ["MLFLOW_TRACKING_PASSWORD"] = DAGSHUB_TOKEN

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    print(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
    print(f"MLflow Experiment: {MLFLOW_EXPERIMENT_NAME}")

    with open(training_output_path) as f:
        data = json.load(f)

    signature = data["signature"]

   
    if mlflow_run_exists(signature):
        raise AirflowSkipException(
            f"MLflow run already exists for signature {signature}"
        )
    
    with mlflow.start_run(run_name=data["training_name"]):

        # Params
        mlflow.log_params(data["params"])

        # Metrics per epoch
        for m in data["metrics"]:
            step = m["epoch"]
            mlflow.log_metric("precision", m["precision"], step=step)
            mlflow.log_metric("recall", m["recall"], step=step)
            mlflow.log_metric("mAP50", m["mAP50"], step=step)
            mlflow.log_metric("mAP50_95", m["mAP50_95"], step=step)

        # Artifact
        mlflow.log_artifact(data["weights_path"],)
        if Path("dvc.yaml").exists():
            mlflow.log_artifact("dvc.yaml", artifact_path="dvc")

        if Path("dvc.lock").exists():
            mlflow.log_artifact("dvc.lock", artifact_path="dvc")
        # Tags
        mlflow.set_tag("training_signature", data["signature"])
        mlflow.set_tag("dvc_remote", value=DVC_REMOTE_NAME)
        mlflow.set_tag("dvc_remote_url", DVC_REMOTE_URL)
        mlflow.set_tag("orchestrator", "airflow")
        
                        
        print("YOLO training metrics,artifacts logged to DAGHub MLflow successfully.")
    print("MLflow Logger task Completed")

        

from airflow.exceptions import AirflowSkipException
from pipelines.training_params import YOLOTrainingParams
from utils.airflow_config import PROCESSED_DATASET, MODEL_PATH, DATASET_DIR, YOLO_RUNS_DIR, MLRUNS_DIR
from pipelines.training_fingerprint import generate_training_signature
from pipelines.mlflow_dedup import (training_already_done,register_training)
from pathlib import Path


done_file = PROCESSED_DATASET / ".done"
data_yaml = DATASET_DIR / "data.yaml"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def check_dataset_ready():    
    if not done_file.exists():
        raise AirflowSkipException("Dataset not ready")

    if not data_yaml.exists():
        raise FileNotFoundError("data.yaml not found")

    print("Dataset is ready for training")


def train_yolo_model():
    import torch
    import json
    from ultralytics import YOLO
    
    if not done_file.exists():
        raise AirflowSkipException("Dataset not ready")

    if not data_yaml.exists():
        raise FileNotFoundError("data.yaml not found")

    print("Dataset is ready for training")

    params = YOLOTrainingParams().to_dict()

    signature = generate_training_signature(
        MODEL_PATH,
        data_yaml,
        params
    )
    if training_already_done(signature):
        raise AirflowSkipException(
        f"Training already completed for signature {signature}"
    )


    model = YOLO(MODEL_PATH)

    epoch_metrics = []

    def on_epoch_end(trainer):
        m = trainer.metrics
        epoch_metrics.append({
            "epoch": trainer.epoch,
            "precision": float(m.get("metrics/precision(B)", 0)),
            "recall": float(m.get("metrics/recall(B)", 0)),
            "mAP50": float(m.get("metrics/mAP50(B)", 0)),
            "mAP50_95": float(m.get("metrics/mAP50-95(B)", 0)),
        })

    model.add_callback("on_fit_epoch_end", on_epoch_end)

    model.train(
        data=str(data_yaml),
        epochs=params["epochs"],
        imgsz=params["imgsz"],
        batch=params["batch"],
        device="cuda" if torch.cuda.is_available() else "cpu",
        workers=0,
        project=str(YOLO_RUNS_DIR),
        name=params["training_name"],
        exist_ok =True
    )


    output_dir = YOLO_RUNS_DIR / params["training_name"]

    training_output = {
        "training_name": params["training_name"],
        "signature": signature,
        "params": params,
        "metrics": epoch_metrics,
        "weights_path": str(output_dir / "weights" / "best.pt"),
    }

    output_path = output_dir / "training_output.json"

    with open(output_path, "w") as f:
        json.dump(training_output, f, indent=2)

    print(f"Training output saved → {output_path}")

    register_training(
    signature,
    {
        "training_name": params["training_name"],
        "weights_path": str(output_dir / "weights" / "best.pt"),
        "params": params,
        "dataset": str(data_yaml),
    }
)

    return str(output_path)
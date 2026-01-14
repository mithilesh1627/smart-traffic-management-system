import subprocess
import mlflow
from airflow.exceptions import AirflowSkipException
from pipelines.training_params import YOLOTrainingParams
from utils.airflow_config import PROCESSED_DATASET, MODEL_PATH,DATASET_DIR
from pipelines.training_fingerprint import generate_training_signature
from pipelines.mlflow_dedup import training_already_done
from pathlib import Path

done_file = PROCESSED_DATASET / ".done"
data_yaml = DATASET_DIR / "data.yaml"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def get_dvc_dataset_hash():
    return subprocess.check_output(
        ["dvc", "rev-parse", "HEAD"],
        cwd=PROJECT_ROOT,
        text=True
    ).strip()

def check_dataset_ready():    
    if not done_file.exists():
        raise AirflowSkipException("Dataset not ready")
    print(" Dataset is ready for training")


def train_yolo_model():
    if not data_yaml.exists():
        raise FileNotFoundError("data.yaml not found")
    
    params_obj = YOLOTrainingParams()
    params = params_obj.to_dict()

    #  Generate fingerprint
    signature = generate_training_signature(
        MODEL_PATH,
        data_yaml,
        params
    )

    #  Check for duplicate training
    if training_already_done(signature):
        raise AirflowSkipException(
            "Identical training configuration already exists in MLflow"
        )

    mlflow.set_experiment("Smart-Traffic-YOLO")

    with mlflow.start_run(run_name="yolo_training") as run:
        mlflow.log_param("training_signature", signature)
        mlflow.log_params(params)

        print(" Starting YOLO training")

        cmd = [
            "yolo",
            "task=detect",
            "mode=train",
            f"model={MODEL_PATH}",
            f"data={data_yaml}",
            f"epochs={params['epochs']}",
            f"imgsz={params['imgsz']}",
            f"batch={params['batch']}",
            f"device={params['device']}",
            "project=mlruns/yolo",
            "name=traffic_yolo_v1",
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        #  Stream YOLO logs into Airflow UI
        for line in process.stdout:
            print(line.rstrip())

        process.wait()

        if process.returncode != 0:
            mlflow.set_tag("training_status", "failed")
            raise RuntimeError(" YOLO training failed")

        mlflow.set_tag("training_status", "success")

        print(" YOLO model training completed successfully")

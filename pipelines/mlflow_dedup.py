import json,mlflow
from utils.airflow_config import MLFLOW_EXPERIMENT_NAME, TRAINING_REGISTRY

def training_already_done(signature: str) -> bool:
    return (TRAINING_REGISTRY / f"{signature}.json").exists()


def register_training(signature: str, metadata: dict):
    path = TRAINING_REGISTRY / f"{signature}.json"
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Registered training with signature {signature} at {path}")

def mlflow_run_exists(signature: str) -> bool:
    client = mlflow.tracking.MlflowClient()

    experiment = client.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
    if experiment is None:
        return False

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string=f"tags.training_signature = '{signature}'",
        max_results=1,
    )

    return len(runs) > 0
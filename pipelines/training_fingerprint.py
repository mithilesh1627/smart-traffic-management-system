import hashlib
import json
import subprocess
from pathlib import Path
from utils.airflow_config import PROJECT_ROOT


def get_dvc_dataset_hash():
    return subprocess.check_output(
        ["git", "hash-object", "IDD_Dataset.dvc"],
        cwd=PROJECT_ROOT,
        text=True
    ).strip()

def file_hash(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def generate_training_signature(
    model_path,
    data_yaml ,
    params
):
    payload = {
        "model": str(model_path),
        "data_yaml_hash": file_hash(data_yaml),
        "dvc_commit": get_dvc_dataset_hash(),
        "params": params,
    }

    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()

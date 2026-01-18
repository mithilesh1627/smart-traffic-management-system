import hashlib
import json
import subprocess
from pathlib import Path
from utils.airflow_config import PROJECT_ROOT

def get_git_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT,
            text=True
        ).strip()
    except Exception as e:
        print(f"[WARN] Git hash not available: {e}")
        return "not_available"

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
        "dvc_commit": get_git_commit_hash(),
        "params": params,
    }

    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()


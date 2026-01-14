import subprocess
import mlflow
from pathlib import Path

def get_git_commit():
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"]
    ).decode().strip()

def get_dvc_commit():
    return subprocess.check_output(
        ["dvc", "status", "-c"]
    ).decode().strip()

def get_dvc_remote():
    return subprocess.check_output(
        ["dvc", "remote", "default"]
    ).decode().strip()

def log_dvc_metadata(dataset_path: Path):
    mlflow.log_param("dataset_path", str(dataset_path))
    mlflow.log_param("git_commit", get_git_commit())
    mlflow.log_param("dvc_remote", get_dvc_remote())

    # log DVC files for reproducibility
    if Path("dvc.yaml").exists():
        mlflow.log_artifact("dvc.yaml", "dvc")

    if Path("dvc.lock").exists():
        mlflow.log_artifact("dvc.lock", "dvc")

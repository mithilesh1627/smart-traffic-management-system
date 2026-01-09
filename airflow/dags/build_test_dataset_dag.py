from airflow.decorators import task, dag
from datetime import datetime
from pathlib import Path
from pipelines.train_dataset_builder import build_train_dataset
from pipelines.test_dataset_builder import build_test_dataset
from pipelines.valid_dataset_builder import build_valid_dataset
from pipelines.dataset_labeling import auto_labeling
from pipelines.mlflow_tracking import track_dataset_stats
from utils.airflow_config import DATASET_DIR
default_args ={
        "owner": "Mithilesh Chaurasiya",
        "retries": 1,
    }

@dag(
    dag_id="build_dataset_dag",
    start_date=datetime(2024, 1, 8),
    catchup=False,
    tags=["dataset", "labeling"],
    default_args= default_args,  
    )
def build_dataset_dag():
    @task
    def preprocess():
        print("Preprocessing dataset...")
        raw_dir = DATASET_DIR
        if not raw_dir.exists():
            raise FileNotFoundError("Raw dataset not found")

    @task
    def build_train_dataset_task():
        build_train_dataset()


    @task
    def build_test_dataset_task():
        build_test_dataset()

    @task
    def build_valid_dataset_task():
        build_valid_dataset()

    @task
    def track_dataset_stats_task():
        track_dataset_stats()
    @task
    def auto_labeling_task():
        auto_labeling()

    raw = preprocess()
    train_task = build_train_dataset_task()
    test_task = build_test_dataset_task()
    valid_task = build_valid_dataset_task()
    mlflow_task = track_dataset_stats_task()
    auto_label = auto_labeling_task()

    raw >>[train_task , test_task , valid_task]
    [train_task , test_task , valid_task] >> mlflow_task >> auto_label
dag = build_dataset_dag()

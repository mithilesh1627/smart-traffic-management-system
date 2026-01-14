from airflow.decorators import task, dag
from datetime import datetime
from pipelines.mark_dataset_ready import mark_dataset_ready
from pipelines.train_dataset_builder import build_train_dataset
from pipelines.test_dataset_builder import build_test_dataset
from pipelines.valid_dataset_builder import build_valid_dataset
from pipelines.dataset_labeling import auto_labeling
# from pipelines.mlflow_tracking import track_dataset_stats
from utils.airflow_config import DATASET_DIR, TEST_SPLIT_METADATA

default_args ={
        "owner": "Mithilesh Chaurasiya",
        "retries": 1,
    }

@dag(
    dag_id="Dataset_Builder_dag",
    start_date=datetime(2024, 1, 15),
    catchup=False,
    tags=["dataset", "labeling","training","preprocessing","train","valid"],
    default_args= default_args,  
    )
def build_dataset_dag():
    @task
    def preprocess():
        print("Preprocessing dataset...")
        print("Checking dataset paths...")
        print(f"DATASET_DIR: {DATASET_DIR}")
        print(f"TEST_SPLIT_METADATA: {TEST_SPLIT_METADATA}")

        if DATASET_DIR is None:
            raise ValueError("DATASET_DIR env variable is not set")

        if not DATASET_DIR.exists():
            raise FileNotFoundError(f"Dataset directory not found: {DATASET_DIR}")

        if not TEST_SPLIT_METADATA.exists():
            raise FileNotFoundError("test.txt not found")
        
        print("Dataset preprocessing completed.")

    @task
    def build_train_dataset_task():
        
        build_train_dataset()


    @task
    def build_test_dataset_task():
        build_test_dataset()

    @task
    def build_valid_dataset_task():
        build_valid_dataset()

    # @task
    # def track_dataset_stats_task():
    #     track_dataset_stats()
    @task
    def auto_labeling_task():
        auto_labeling()
    
    @task
    def mark_dataset_ready_task():
        mark_dataset_ready()

    raw = preprocess()
    train_task = build_train_dataset_task()
    test_task = build_test_dataset_task()
    valid_task = build_valid_dataset_task()
    # mlflow_task = track_dataset_stats_task()
    auto_label = auto_labeling_task()
    mark_ready = mark_dataset_ready_task()

    raw >>[train_task , test_task , valid_task]
    [train_task , test_task , valid_task] >> auto_label >> mark_ready
dag = build_dataset_dag()

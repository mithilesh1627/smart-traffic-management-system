from airflow.decorators import task, dag
from datetime import datetime
from pipelines.dataset_cleaner import clean_dataset
from pipelines.dataset_validator import validate_labels_required, validate_structure_only
from pipelines.mark_dataset_ready import mark_dataset_ready
from pipelines.train_dataset_builder import build_train_dataset
from pipelines.test_dataset_builder import build_test_dataset
from pipelines.valid_dataset_builder import build_valid_dataset
from pipelines.dataset_labeling import auto_labeling
from pipelines.dataset_validator import validate_structure_only
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
    schedule="0 0 * * *", 
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

    @task
    def auto_labeling_task():
        auto_labeling()
    @task
    def validate_structure_task():
        validate_structure_only()

    @task
    def mark_dataset_ready_task():
        mark_dataset_ready()

    @task
    def validate_labels_task():
        validate_labels_required()
    @task
    def clean_unlabeled_images_task():
        clean_dataset()

    raw = preprocess()
    train_task = build_train_dataset_task()
    test_task = build_test_dataset_task()
    valid_task = build_valid_dataset_task()
    validate_structure=validate_structure_task()
    validate_label = validate_labels_task()
    clean_dataset_task = clean_unlabeled_images_task()
    auto_label = auto_labeling_task()
    mark_ready = mark_dataset_ready_task()

    raw >>[train_task , test_task , valid_task]
    [train_task , test_task , valid_task] >> validate_structure >> auto_label >> clean_dataset_task >> validate_label >> mark_ready
dag = build_dataset_dag()

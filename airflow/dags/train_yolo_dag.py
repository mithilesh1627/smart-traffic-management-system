from airflow.decorators import dag, task
from datetime import datetime

default_args = {
    "owner": "Mithilesh Chaurasiya",
    "retries": 1,
}

@dag(
    dag_id="training_YOLO_model_dag",
    start_date=datetime(2024, 1, 14),
    catchup=False,
    tags=["yolo", "training"],
    default_args=default_args,
    schedule="0 2 * * *",
)
def train_yolo_dag():

    @task
    def check_dataset_task():
        from pipelines.yolo_training import check_dataset_ready
        check_dataset_ready()

    @task(retries=0)
    def train_yolo_model_task():
        from pipelines.yolo_training import train_yolo_model
        return train_yolo_model()
   
    @task
    def mlflow_logger_task(training_output_path: str):
        from pipelines.mlflow_yolo_logger import log_yolo_to_mlflow
        log_yolo_to_mlflow(training_output_path)    
    @task
    def validate_train_valid_task():
        from pipelines.dataset_validator import validate_images_train_valid
        validate_images_train_valid()

    # Task dependencies
    check_task = check_dataset_task()
    validate_task = validate_train_valid_task()
    train_task = train_yolo_model_task()
    log_artifacts_task = mlflow_logger_task(train_task)
    

    check_task >> validate_task >> train_task  >> log_artifacts_task

dag = train_yolo_dag()

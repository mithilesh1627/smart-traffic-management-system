from airflow.decorators import dag, task
from datetime import datetime
from pipelines.dataset_validator import validate_images_train_valid
from pipelines.mlflow_yolo_logger import log_yolo_model
from pipelines.yolo_training import check_dataset_ready, train_yolo_model


default_args ={
        "owner": "Mithilesh Chaurasiya",
        "retries": 1,
    }

@dag(
    dag_id="training_YOLO_model_dag",
    start_date=datetime(2024, 1, 14),
    catchup=False,
    tags=["yolo", "training"],
    default_args= default_args,
    )

def train_yolo_dag():

    @task
    def check_dataset():
        check_dataset_ready()

    @task(retries=0)
    def train_yolo_model_task():
        train_yolo_model()
        
    @task
    def log_yolo_model_task():
        log_yolo_model()
    
    @ task 
    def validate_images_train_valid_task():
        validate_images_train_valid()

    check_dataset_task = check_dataset()
    train_task = train_yolo_model_task()
    log_model_task = log_yolo_model_task()
    validate_images_task = validate_images_train_valid_task()
    check_dataset_task>>validate_images_task >> train_task >> log_model_task

dag = train_yolo_dag()
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/mithilesh/airflow/project")
sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.valid_dataset_builder import build_valid_dataset

default_args  = {
    'owner':'Mithilesh Chaurasiya',
    'retries':1
}

with DAG(
    dag_id='build_valid_dataset_dag',
    description='Prepare the valid image dataset for Smart Traffic Management System',
    default_args=default_args,
    start_date=datetime(2026,1,4),
    catchup=False,
    schedule=None,
    tags=["dataset", "cv", "traffic",'valid','images']
    ) as dag:

    build_valid_data = PythonOperator(
        task_id = 'build_valid_dataset_task',
        python_callable = build_valid_dataset
    )
    build_valid_data
    

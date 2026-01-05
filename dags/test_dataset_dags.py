from airflow import DAG
from pathlib import Path
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
PROJECT_ROOT = Path("/home/mithilesh/airflow/project")
sys.path.insert(0, str(PROJECT_ROOT))
from pipelines.test_dataset_builder import build_test_dataset

default_args  = {
    'owner':'Mithilesh Chaurasiya',
    'retries':1
}

with DAG(
    dag_id='build_test_dataset_dag',
    description='Prepare the test image dataset for Smart Traffic Management System',
    default_args=default_args,
    start_date=datetime(2026,1,4),
    catchup=False,
    tags=["dataset", "cv", "traffic",'test','images']
    ) as dag:

    build_test_data = PythonOperator(
        task_id = 'build_test_dataset_task',
        python_callable = build_test_dataset
    )
    build_test_data
    

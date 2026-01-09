# dags/traffic_pipeline_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
default_args  = {
    'owner':'Mithilesh Chaurasiya',
    'retries':1
}
with DAG(
    dag_id="smart_traffic_pipeline",
    start_date=datetime(2025, 1, 3),
    default_args=default_args,
    catchup=False,
    tags=["dataset", "cv", "traffic",'test','test','train','images']
    ) as dag:

    run_pipeline = BashOperator(
        task_id="run_inference_pipeline",
        bash_command="""
cd /mnt/d/2026/CV_Project/smart-traffic-management-system &&
python -m inference.pipeline
""")

    run_pipeline

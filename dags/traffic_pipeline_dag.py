# dags/traffic_pipeline_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="smart_traffic_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    run_pipeline = BashOperator(
        task_id="run_inference_pipeline",
        bash_command="cd /opt/project && python -m inference.pipeline"
    )

    run_pipeline

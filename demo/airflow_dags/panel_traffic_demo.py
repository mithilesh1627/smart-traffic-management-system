"""Real local inference demonstration, using Windows services through WSL interop."""
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

PYTHON = '/mnt/d/2026/smart-traffic-management-system/.venv-demo/Scripts/python.exe'
ROOT = 'D:/2026/smart-traffic-management-system/demo'
with DAG('panel_traffic_live_demo', start_date=datetime(2026, 1, 1),
         schedule=None, catchup=False, max_active_runs=1,
         tags=['panel-demo', 'base-yolo', 'real-inference'],
         description='Check services, run base YOLO inference + aggregation, verify MongoDB output.') as dag:
    check = BashOperator(task_id='check_local_services', bash_command=f'{PYTHON} {ROOT}/check.py')
    inference = BashOperator(task_id='run_yolo_and_store_analytics',
        bash_command=f'{PYTHON} {ROOT}/run_video.py --execution-source "Airflow panel_traffic_live_demo"')
    verify = BashOperator(task_id='verify_saved_results', bash_command=f'{PYTHON} {ROOT}/verify_airflow.py')
    check >> inference >> verify

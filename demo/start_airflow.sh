#!/usr/bin/env bash
set -e
export AIRFLOW_HOME="$HOME/airflow-panel-demo"
export AIRFLOW__CORE__DAGS_FOLDER=/mnt/d/2026/smart-traffic-management-system/demo/airflow_dags
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
export PYTHONPATH=/mnt/d/2026/smart-traffic-management-system
export AIRFLOW_VAR_PROJECT_ROOT=/mnt/d/2026/smart-traffic-management-system
export AIRFLOW__CORE__EXECUTOR=SequentialExecutor
export AIRFLOW__WEBSERVER__WEB_SERVER_PORT=8080
export AIRFLOW__WEBSERVER__WEB_SERVER_HOST=0.0.0.0
export PATH="$HOME/airflow/airflow_env/bin:$PATH"
mkdir -p "$AIRFLOW_HOME"
ln -sfn /mnt/d/2026/smart-traffic-management-system/airflow/dags "$AIRFLOW__CORE__DAGS_FOLDER/project_dags"
if ! pgrep -f 'airflow standalone' >/dev/null; then
    nohup airflow standalone > "$AIRFLOW_HOME/startup.log" 2>&1 < /dev/null &
    sleep 5
    echo "Started Airflow; log: $AIRFLOW_HOME/startup.log"
else
    echo 'Airflow standalone is already running.'
fi

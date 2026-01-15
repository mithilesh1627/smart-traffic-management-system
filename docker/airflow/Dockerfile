FROM apache/airflow:2.8.1-python3.10

USER root

# System deps
RUN apt-get update && apt-get install -y \
    libgl1 \
    git \
    && apt-get clean

# Python deps
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Project code
COPY airflow /opt/airflow/dags
COPY pipelines /opt/airflow/pipelines
COPY utils /opt/airflow/utils
COPY traffic_metrics /opt/airflow/traffic_metrics

ENV PYTHONPATH="/opt/airflow"

USER airflow

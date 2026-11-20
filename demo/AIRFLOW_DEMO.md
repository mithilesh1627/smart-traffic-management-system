# Airflow live demo

Open http://localhost:8080. Username: `admin`.
Retrieve the generated local password in PowerShell:

```powershell
wsl -d Ubuntu-22.04 -- cat /home/mithilesh/airflow-panel-demo/standalone_admin_password.txt
```

Select `panel_traffic_live_demo`, open Graph, then click the play button / Trigger DAG.
Watch these tasks turn green:

1. `check_local_services`: checks Streamlit, MLflow, and MongoDB.
2. `run_yolo_and_store_analytics`: processes the six-second traffic sample with base YOLO, saves real metrics, aggregates them, and logs an MLflow run.
3. `verify_saved_results`: verifies saved metrics and the Airflow execution marker in MongoDB.

Click a task and open Logs to show its actual output. Then show http://localhost:8501 and http://localhost:5000.

This is a separate local demonstration DAG, not a run of the original training/preprocessing DAGs. It uses base `yolo11n.pt`; it does not demonstrate custom-trained accuracy or training. Original Airflow metadata is preserved; demo metadata lives in Ubuntu at `~/airflow-panel-demo`.

To restart from PowerShell:

```powershell
cd D:\2026\smart-traffic-management-system
.\Start_Airflow_Demo.ps1
```

Airflow may take around 30 seconds to start. This guide supersedes earlier statements that Airflow is unavailable in the local demo.

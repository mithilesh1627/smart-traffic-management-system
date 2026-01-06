import mlflow
import mlflow.pyfunc
from pathlib import Path

class MLflowTracker:
    def __init__(
        self,
        experiment_name,
        camera_id,
        model_name,
        metric_interval
    ):
        mlflow.set_experiment(experiment_name)

        self.run = mlflow.start_run(run_name=f"{camera_id}_{model_name}")

        mlflow.log_param("camera_id", camera_id)
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("metric_interval_sec", metric_interval)
        mlflow.log_param("tracker", "ByteTrack")

    def log_metrics(self, flow, density, vehicle_count):
        mlflow.log_metric("avg_flow", flow)
        mlflow.log_metric("avg_density", density)
        mlflow.log_metric(
            "total_vehicles",
            sum(vehicle_count.values())
        )

    def log_artifact(self, path):
        mlflow.log_artifact(path)

    def close(self):
        mlflow.end_run()

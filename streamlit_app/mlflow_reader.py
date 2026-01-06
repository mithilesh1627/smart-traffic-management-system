import mlflow
import pandas as pd

def load_mlflow_runs(experiment_name):
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        return pd.DataFrame()

    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    return runs

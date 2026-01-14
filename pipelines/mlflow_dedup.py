from mlflow.tracking import MlflowClient

def training_already_done(signature: str) -> bool:
    client = MlflowClient()
    exp = client.get_experiment_by_name("Smart-Traffic-YOLO")

    if not exp:
        return False

    runs = client.search_runs(
        experiment_ids=[exp.experiment_id],
        filter_string=f"params.training_signature = '{signature}'",
        max_results=1
    )
    return len(runs) > 0

import mlflow
from pathlib import Path
from utils.airflow_config import TRAIN_IMG_DIR, TEST_IMG_DIR, VALID_IMG_DIR, DATASET_DIR

def track_dataset_stats():
    mlflow.set_experiment("Smart-Traffic-Dataset-Pipeline")

    with mlflow.start_run(run_name="dataset_preparation"):

        train_images = TRAIN_IMG_DIR
        test_images  = TEST_IMG_DIR
        valid_images = VALID_IMG_DIR

        def count_images(path: Path):
            return len(list(path.glob("*.jpg")))

        train_count = count_images(train_images)
        test_count  = count_images(test_images)
        valid_count = count_images(valid_images)

        # Log metrics
        mlflow.log_metric("train_images", train_count)
        mlflow.log_metric("test_images", test_count)
        mlflow.log_metric("valid_images", valid_count)

        # Log params
        mlflow.log_param("dataset_name", "IDD")
        mlflow.log_param("task", "object_detection")

        # Log dataset path as artifact
        mlflow.log_artifact(str(DATASET_DIR), artifact_path="Processed_Dataset")

        print("MLflow dataset tracking completed")

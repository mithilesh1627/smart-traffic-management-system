from utils.airflow_config import PROCESSED_DATASET

def mark_dataset_ready():
    """
    Creates a .done file to signal dataset is ready for training
    """
    done_file = PROCESSED_DATASET / ".done"
    done_file.parent.mkdir(parents=True, exist_ok=True)
    done_file.touch()
    print(f" Dataset marked ready: {done_file}")

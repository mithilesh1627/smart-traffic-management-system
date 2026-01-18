from datetime import datetime
from utils.mongo_helper import get_collection
from utils.config import (
    MONGO_URI,
    DB_NAME,
    INFERENCE_COLLECTION_NAME,
)

def store(**kwargs):
    """
    Store aggregated analytics safely (idempotent).
    """

    ti = kwargs["ti"]
    doc = ti.xcom_pull(task_ids="aggregate_metrics")

    if not doc:
        print("No aggregated document to store.")
        return

    col = get_collection(
        MONGO_URI,
        DB_NAME,
        INFERENCE_COLLECTION_NAME
    )

    doc["created_at"] = datetime.utcnow()

    unique_filter = {
        "camera_id": doc["camera_id"],
        "window_size": doc["window_size"],
        "start_time": doc["start_time"],
        "end_time": doc["end_time"],
    }

    col.update_one(
        unique_filter,
        {"$set": doc},
        upsert=True
    )

    print(
        f"Stored analytics | "
        f"Camera={doc['camera_id']} | "
        f"Window={doc['start_time']} → {doc['end_time']}"
    )

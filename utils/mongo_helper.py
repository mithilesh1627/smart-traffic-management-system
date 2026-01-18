from pymongo import MongoClient, errors
from datetime import datetime, timedelta

from pyparsing import col

# ---------------- Connect to cluster ----------------
_client = None

def get_mongo_client(uri: str):
    global _client
    if _client is None:
        _client = MongoClient(uri)
    return _client
# ---------------- Get collection ----------------
def get_collection(uri: str, db_name="traffic_system", collection_name="metrics"):
    client = get_mongo_client(uri)
    db = client[db_name]
    col = db[collection_name]

    # ensure indexes
    col.create_index("camera_id")
    col.create_index("start_time")
    col.create_index("end_time")

    return col

# ---------------- Store metrics ----------------
def store_metrics(collection, camera_id: str, metrics: dict):
    document = {
        "camera_id": camera_id,
        "timestamp": metrics.get("timestamp", datetime.utcnow()),
        "vehicle_count": metrics.get("vehicle_count", 0),
        "flow": metrics.get("flow", 0),
        "density": metrics.get("density", 0),
    }
    collection.insert_one(document)



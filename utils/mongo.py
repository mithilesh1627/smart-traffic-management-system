from pymongo import MongoClient

def get_collection(uri):
    client = MongoClient(uri)
    db = client["traffic_system"]
    col = db["metrics"]

    col.create_index("timestamp")
    col.create_index("camera_id")

    return col

def store_metrics(collection, camera_id, metrics):
    document = {
        "camera_id": camera_id,
        "timestamp": metrics["timestamp"],
        "vehicle_count": metrics["vehicle_count"],
        "flow": metrics["flow"],
        "density": metrics["density"]
    }
    collection.insert_one(document)

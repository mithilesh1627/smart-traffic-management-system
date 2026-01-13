from pymongo import MongoClient
import pandas as pd

def load_metrics(uri, db, collection, camera_id=None, limit=500):
    client = MongoClient(uri)
    col = client[db][collection]

    query = {}
    if camera_id:
        query["camera_id"] = camera_id

    cursor = (
        col.find(query, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )

    data = list(cursor)
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp")

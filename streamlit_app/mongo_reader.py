from pymongo import MongoClient
import pandas as pd

def load_metrics(uri, db, collection, limit=500):
    client = MongoClient(uri)
    col = client[db][collection]

    cursor = (
        col.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )

    df = pd.DataFrame(list(cursor))
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df.sort_values("timestamp")

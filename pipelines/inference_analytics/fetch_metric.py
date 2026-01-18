from utils.mongo_helper import get_collection
from datetime import datetime, timedelta
from utils.config import MONGO_URI, DB_NAME, INFERENCE_COLLECTION_NAME
# ---------------- Fetch metrics ----------------
def fetch_metrics(hours=1):
    print("Connecting to MongoDB to fetch metrics...")
    col = get_collection(MONGO_URI, DB_NAME, INFERENCE_COLLECTION_NAME)
    print(f"Fetching metrics from MongoDB for the last {hours} hour(s)...")
    end = datetime.utcnow()
    start = end - timedelta(hours=hours)
    
    print(f"Fetched documents from MongoDB.")
    return {
        "window_size": f"{hours}h",
        "start": start.isoformat(),
        "end": end.isoformat()
    }
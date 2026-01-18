import random
from datetime import datetime, timedelta
from utils.mongo_helper import get_collection
from utils.config import MONGO_URI, DB_NAME, INFERENCE_COLLECTION_NAME

CAMERA_IDS = ["usb_0", "usb_1", "rtsp_01"]

col = get_collection(
    MONGO_URI,
    DB_NAME,
    INFERENCE_COLLECTION_NAME
)

now = datetime.utcnow()
docs = []

for i in range(60):  # last 60 minutes
    ts = now - timedelta(minutes=60 - i)

    for cam in CAMERA_IDS:
        doc = {
            "camera_id": cam,
            "timestamp": ts,

            "vehicle_count_interval": {
                "car": random.randint(2, 10),
                "bike": random.randint(1, 6),
                "truck": random.randint(0, 2),
            },

            "flow": round(random.uniform(0.3, 1.2), 2),
            "density": round(random.uniform(0.2, 0.9), 2),
        }

        docs.append(doc)

col.insert_many(docs)

print(f"Inserted {len(docs)} fake inference metrics")

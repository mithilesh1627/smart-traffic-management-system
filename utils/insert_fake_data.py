import random
from datetime import datetime, timedelta
from utils.mongo import get_collection
from utils.config import MONGO_URI, DB_NAME, COLLECTION_NAME

CAMERA_IDS = ["usb_0", "usb_1", "rtsp_01"]
VEHICLE_CLASSES = ["car", "truck", "bus", "motorcycle"]

# collection = get_collection(MONGO_URI)

# # ---------------- FAKE DATA ----------------
# def generate_vehicle_counts(base):
#     return {
#         cls: base[cls] + random.randint(0, 5)
#         for cls in VEHICLE_CLASSES
#     }

# def generate_interval_delta():
#     return {
#         cls: random.randint(0, 3)
#         for cls in VEHICLE_CLASSES
#         if random.random() > 0.5
#     }

# base_counts = {
#     "car": 100,
#     "truck": 20,
#     "bus": 10,
#     "motorcycle": 40
# }

# start_time = datetime.utcnow() - timedelta(hours=1)

# docs = []

# for i in range(60):  # 60 records (1 per minute)
#     for camera_id in CAMERA_IDS:
#         base_counts = generate_vehicle_counts(base_counts)

#         doc = {
#             "camera_id": camera_id,
#             "timestamp": start_time + timedelta(minutes=i),
#             "vehicle_count_total": base_counts,
#             "vehicle_count_interval": generate_interval_delta(),
#             "flow": round(random.uniform(2.0, 10.0), 2),
#             "density": round(random.uniform(0.1, 0.9), 2)
#         }

#         docs.append(doc)

# # ---------------- INSERT ----------------
# collection.insert_many(docs)

# print(f"Inserted {len(docs)} fake traffic records ")


from pymongo import MongoClient
from pprint import pprint

client = MongoClient(MONGO_URI)
col = client[DB_NAME][COLLECTION_NAME]

print(col.count_documents({}))
pprint(col.find_one())
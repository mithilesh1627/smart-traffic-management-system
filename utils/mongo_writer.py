
from utils.mongo import get_collection

class MongoWriter:
    def __init__(self, mongo_uri):
        try:
            self.collection = get_collection(mongo_uri)
        except Exception as e:
            raise RuntimeError(f"MongoDB connection failed: {e}")

    def write(self, doc):
        if doc:
            self.collection.insert_one(doc)
            print("[INFO] Metrics stored:", doc)

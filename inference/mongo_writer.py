
from utils.mongo import get_collection

class MongoWriter:
    def __init__(self, mongo_uri):
        self.collection = get_collection(mongo_uri)

    def write(self, doc):
        if doc:
            self.collection.insert_one(doc)
            print("[INFO] Metrics stored:", doc)

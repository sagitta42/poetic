from pymongo import MongoClient

from core.mongo_config import get_mongo_config
from core.models.mongo_document import MyMongoDocument


class MyMongoDB:
    def __init__(self) -> None:
        # TODO:
        # document_class: default class to use for
        # documents returned from queries on this client

        config = get_mongo_config()
        self.client = MongoClient(**config.model_dump())
        self.collection = self.client["lia"].neural_networks

    def append(self, document: MyMongoDocument):
        self.collection.insert_one(
            {
                "_id": nn.id,
                **nn.model_dump(),
                "result": None,
                "created_at": self.now,
                "updated_at": self.now,
            }
        )

    def update(self, document: MyMongoDocument):
        self.collection.update_one(
            {"_id": document.id},
            {"$set": document.model_dump() | {"updated_at": self.now}},
        )

    def get(self, id: str) -> MyMongoDocument | None:
        dct = self.collection.find_one({"_id": id})
        if dct is None:
            return None
        for key in ["created_at", "updated_at", "_id"]:
            dct.pop(key)
        ret = MyMongoDocument(**dct)
        return ret


mongo_db = MyMongoDB()

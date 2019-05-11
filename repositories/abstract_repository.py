from pymongo import MongoClient
from bson.objectid import ObjectId
from entities import UserEntity

class AbstractRepository:
    def __init__(self, entity_name):
        # client = MongoClient('mongodb://[user]:[password]@[host]:[port]')
        client = MongoClient('mongodb://future:future@localhost:27017')
        self.db = client.progjar[entity_name]

    def find_by_id(self, id):
        return self.db.find_one({
            '_id': ObjectId(id)
        })

    def save(self, entity_obj):
        if entity_obj.id is None:
            id = ObjectId()
            self.db.insert_one(entity_obj.get_data())
            entity_obj.id = id

        else:
            self.db.update_one(
                {'_id': entity_obj.id},
                entity_obj.get_data()
            )

import entities

from bson.objectid import ObjectId
from pymongo import MongoClient

from env import Env


class AbstractRepository:
    mongo_connection = None

    def __init__(self, entity_name):

        if AbstractRepository.mongo_connection is None:
            # client = MongoClient('mongodb://[user]:[password]@[host]:[port]')
            AbstractRepository.mongo_connection = MongoClient(
                'mongodb://'+Env.mongodb_user+':'
                +Env.mongodb_password+'@'
                +Env.mongodb_host+':'
                +str(Env.mongodb_port)
            )
        self.db = AbstractRepository.mongo_connection[Env.mongodb_database][entity_name]

    def find_by_code(self, id: str) -> dict:
        return self.db.find_one({
            '_id': ObjectId(id)
        })

    def save(self, entity_obj: entities.BaseEntity):
        if entity_obj.id is None:
            id = ObjectId()
            self.db.insert_one(entity_obj.get_data())
            entity_obj.id = id

        else:
            self.db.update_one(
                {
                    '_id': ObjectId(entity_obj.id)
                },
                {
                    "$set": entity_obj.get_data()
                }
            )

        return entity_obj.id
            

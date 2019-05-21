import pymongo
from pymongo import MongoClient

from env import Env

conn = MongoClient(
                'mongodb://'+Env.mongodb_user+':'
                +Env.mongodb_password+'@'
                +Env.mongodb_host+':'
                +str(Env.mongodb_port)
            )

db = conn.progjar['users']

db.update_one({
    '_id' :
})


import pymongo
import os

class Database:

    def __init__(self, db_name=False):

        if os.environ.get('PRODUCTION') == 'S':
            self.client = pymongo.MongoClient(os.environ.get('PRODUCTION_CONNECTION'))
        else:
            self.client = pymongo.MongoClient(os.environ.get('LOCAL_CONNECTION'))
        
        if not db_name:
            db_name = os.environ.get('DB_NAME')

        self.db = self.client.get_database(db_name)

    def insert(self, col_name, object):
        coll = self.db.get_collection(col_name)

        coll.insert_one(object)
    
    def update(self, col_name, object, query):
        coll = self.db.get_collection(col_name)

        coll.update_one(query, {'$set': object}, upsert=True)
    
    def delete(self, col_name, query):
        coll = self.db.get_collection(col_name)

        coll.delete_one(query)
    
    def find_object(self, col_name, query):
        coll = self.db.get_collection(col_name)

        return coll.find(query)

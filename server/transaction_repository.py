import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from mongo_schemas.transaction_schema import Transaction
from mongo_schemas.cursor_schema import Cursor
import logging
from typing import Optional
from datetime import datetime, timedelta


load_dotenv()

# cluster = MongoClient(os.getenv("MONGO_CLIENT"))

# db = cluster["plaid-app"]
# main_collection = db["transactions"]

# main_collection.insert_one({"_id":0,"name":"krishiv"})

class TransactionRepository:
    """
    Deal with saving saving documents in monogdb main_collection "transactions" 
    """

    #TODO: pass in the os.getenv thingy when invoking init ("MONGOCLIENT")
    def __init__(self, cluster_name, db_name, main_collection_name,cursor_collection_name) -> None:
        self.cluster = MongoClient(cluster_name)
        self.db = self.cluster[db_name]
        self.main_collection = self.db[main_collection_name]
        self.cursor_collection = self.db[cursor_collection_name]
        logging.info(f"Successfully connected to MongoDB main_collection: {main_collection_name}")
    

    def save_transactions(self, transaction_array:list[Transaction]) -> bool:
        """
        saves transactions
        args:
            transactions: array of transaction objects
        returns: duh
        """
        self.main_collection.insert_many([i.to_dict() for i in transaction_array])
        return True

    def save_cursor(self, cursor: Cursor) -> bool:
        self.cursor_collection.update_one(
            {"access_token": cursor.access_token},  # find by access_token
            {"$set": cursor.to_dict()}, # update/insert cursor
            upsert=True  # create if nonexistent
        )
    
    def find_cursor(self, access_token:str) -> Optional[Cursor]:
        found = self.cursor_collection.find_one(
            {"access_token":access_token}
        )
        if found:
            return Cursor.from_dict(found)
        return None
    
    def find_transactions(self,access_token:str, lookback:int = 1):
        """
        lookup transactions for the previous
        """
        prev = datetime.now() - timedelta(days=lookback)
        found = self.main_collection.find(
            {
                "date": {"$gt": prev},
                "access_token": access_token
            }
        )
        return [Transaction.from_dict(document) for document in found]
        


# mongodb+srv://kgubba:<db_password>@cluster0.wan6j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
     
        
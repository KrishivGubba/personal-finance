import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from mongo_schemas.transaction_schema import Transaction
import logging

load_dotenv()

# cluster = MongoClient(os.getenv("MONGO_CLIENT"))

# db = cluster["plaid-app"]
# collection = db["transactions"]

# collection.insert_one({"_id":0,"name":"krishiv"})

class TransactionRepository:
    """
    Deal with saving saving documents in monogdb collection "transactions" 
    """

    #TODO: pass in the os.getenv thingy when invoking init ("MONGOCLIENT")
    def __init__(self, cluster_name, db_name, collection_name) -> None:
        print("hi ok doing")
        self.cluster = MongoClient(cluster_name)
        self.db = self.cluster[db_name]
        self.collection = self.db[collection_name]
        logging.info(f"Successfully connected to MongoDB collection: {collection_name}")
    

    def save_transactions(self, transaction_array:list[Transaction]) -> bool:
        """
        saves transactions
        args:
            transactions: array of transaction objects
        returns: duh
        """
        print("definitely doing it now")
        self.collection.insert_many([i.to_dict() for i in transaction_array])
        return True

        


# mongodb+srv://kgubba:<db_password>@cluster0.wan6j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
     
        
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

cluster = MongoClient(os.getenv("MONGO_CLIENT"))

db = cluster["plaid-app"]
collection = db["transactions"]

collection.insert_one({"_id":0,"name":"krishiv"})

class TransactionRepository:
    """
    Deal with saving saving documents in monogdb collection "transactions" 
    """

    def __init__(self) -> None:
        pass
    

    def save_transactions(self,):
        """
        saves transactions

        args:
            transactions: array of transaction objects
        returns:
            true if successful else false
        """


# mongodb+srv://kgubba:<db_password>@cluster0.wan6j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
     
        
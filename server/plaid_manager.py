from dotenv import load_dotenv
import os
import plaid
from plaid.api import plaid_api
from plaid import ApiClient
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from datetime import datetime, timedelta
from mongo_schemas.transaction_schema import Transaction
from mongo_schemas.cursor_schema import Cursor
from transaction_repository import TransactionRepository
from plaid import Configuration, Environment, ApiClient
from typing import Optional
from plaid.api.plaid_api import PlaidApi
import random 
import string
from email_sending import EmailSender

SANDBOX_ACCESS_TEST = "access-sandbox-7b271418-b0a6-43d5-a2cf-2734fc7b84c0"

class PlaidManager:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("PLAID_CLIENT_ID")
        self.secret = os.getenv("PLAID_SECRET")

        configuration = Configuration(
            host=Environment.Sandbox,
            api_key={
                'clientId': self.client_id,
                'secret': self.secret,
            }
        )
        
        api_client = ApiClient(configuration)
        self.client = PlaidApi(api_client)
    
    def create_link_token(self):
        """
        Create a link token for a specific user
        Args:
            user_id: Unique identifier for the user
        Returns:
            link_token: Token string if successful
        """
        try:
            user = LinkTokenCreateRequestUser(client_user_id=PlaidManager.generateRandString(random.randint(1,20)))
            
            request = LinkTokenCreateRequest(
                products=[Products('auth'), Products('transactions')],
                client_name="something",
                country_codes=[CountryCode('US')],
                language='en',
                user=user
            )
            
            response = self.client.link_token_create(request)
            return response.link_token
            
        except plaid.ApiException as e:
            print(f"Error creating link token: {e}")
            print(f"Error detail: {e.body}")
            return None
    
    def create_access_token(self, public_token):
        """
        Create access token for user
        args:
            public_token: sent in from frontend after user auth
        returns:
            access_token: returns permanent key that can be used to access user details
        """
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        access_token = response.access_token
        item_id = response['item_id']
        return access_token
        # except :
        #     print(f"Error creating access token:")
        #     print(f"Error detail")
        #     return None

    def update_transactions(self, access_token:str) -> Optional[tuple[list[Transaction], Cursor]]:
        """
        Update transactions for a user
        args:
            access_token: unique user id
            cursor: last fetched date, if NONE: then will fetch all data
        returns:
            True if success -> and saves transaction and cursor documents
            else False
        """
        try:#TODO: get rid of the cursor argument, we need to lookup in db for it, if doesn't exist, then first time user
            load_dotenv()
            cacher = TransactionRepository(
                                os.getenv("MONGO_CLIENT"), 
                                os.getenv("MONGO_DB_NAME"),
                                os.getenv("MONGO_TRANSACTION_COLLECTION"),
                                os.getenv("MONGO_TRANSACTION_CURSOR_COLLECTION")
                                )
            cursorLookup = cacher.find_cursor(access_token=access_token)
            #if not found, then go ahead without cursor (will fetch all records)
            if not cursorLookup:
                request = TransactionsSyncRequest(
                    access_token=access_token,
                )
            else: request = TransactionsSyncRequest(access_token=access_token, cursor=cursorLookup.cursor)
            
            response = self.client.transactions_sync(request)
            added_transactions = response.added
            
            # weird logic
            yesterday = datetime.now().date() - timedelta(days=1 if cursorLookup else 10000)
            # Filter transactions - convert transaction.date to date if it's datetime
            recent_transactions = [
                transaction for transaction in added_transactions
                if (transaction.date.date() if isinstance(transaction.date, datetime) else transaction.date) > yesterday
            ]
            
            #making transaction objects
            all_transactions = []
            for transaction in recent_transactions:
                transaction["access_token"] = access_token
                all_transactions.append(Transaction.from_dict(transaction))
            #cursor object
            new_cursor = Cursor(access_token, cursor=response["next_cursor"],cursor_type="transactions")
            #TODO: save the cursor and all_transactions by calling methods in transaction_schema
            #transaction saving:
            if all_transactions: cacher.save_transactions(all_transactions)
            #cursor saving:
            cacher.save_cursor(cursor=new_cursor)
            return (all_transactions, new_cursor)
        except plaid.ApiException as e:
            print(f"Error getting transactions: {e}")
            print(f"Error detail: {e.body}")
            return None
    
    def get_prev_transactions(self, access_token:str, days: int) -> dict:
        """
        This fetches transactions by previous days. this is NOT like update_transcations, ie: will not update any records, will not
        call Plaid API, will ONLY fetch records from transactions mongodb collection



        Will also arrange into expenses and income (maybe)

        args:
            days: lookback
            access_token: for specific user transaction lookup
        returns:
            transactions: hmap of transactions, two fields, incoming & outgoing
        """
        fetcher = TransactionRepository(
                                os.getenv("MONGO_CLIENT"), 
                                os.getenv("MONGO_DB_NAME"),
                                os.getenv("MONGO_TRANSACTION_COLLECTION"),
                                os.getenv("MONGO_TRANSACTION_CURSOR_COLLECTION")
                                )
        prevTransactions = fetcher.find_transactions(access_token,days)
        output = {
            "incoming":[],
            "outgoing":[]
        }
        if prevTransactions:
            for transaction in prevTransactions:
                if transaction.amount>=0:
                    output["outgoing"].append(transaction)
                else: output["incoming"].append(transaction)
        return output


    
    @staticmethod
    def generateRandString(length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

# plaid  = PlaidManager()
# output = plaid.get_prev_transactions(SANDBOX_ACCESS_TEST, 15)

# # print(output["incoming"][0].amount)  # This will show all attributes

# sender = EmailSender("kgubba@wisc.edu")
# one, two = sender.render_html(output)
# print(one)
# print(two)
# sender.send_email("krishivgubba626@gmail.com", one, two)




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
import random 
import string

SANDBOX_ACCESS_TEST = "access-sandbox-32c840d8-1f70-4c2e-afe7-2394619a6bdc"

class PlaidManager:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("PLAID_CLIENT_ID")
        self.secret = os.getenv("PLAID_SECRET")
        
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': self.client_id,
                'secret': self.secret,
            }
        )
        
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
    
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
    
    def update_transactions(self, access_token, cursor=""):
        """
        Update transactions for a user
        args:
            access_token: unique user id
            cursor: last fetched date, if NONE: then will fetch all data
        returns:
            ??
        """
        request = TransactionsSyncRequest(
            access_token=access_token,
        )
        print(self.client.transactions_sync(request))

        
    
    @staticmethod
    def generateRandString(length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

plaid  = PlaidManager()
plaid.update_transactions(SANDBOX_ACCESS_TEST, None)
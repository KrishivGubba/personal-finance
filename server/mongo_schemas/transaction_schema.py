from dataclasses import dataclass, asdict
from datetime import date, datetime

"""
transaction_fields = [
    'transaction_id',      # Plaid's unique transaction identifier
    'access_token',       # To identify the user
    'account_id',         # To identify which account
    'amount',            # Transaction amount
    'date',             # Transaction date
    'name',             # Description/merchant name from bank
    'merchant_name',    # When available (often None)
    'category',         # Plaid's category (if available)
    'personal_finance_category',  # More detailed categorization
    'pending',          # Transaction status
    'payment_channel',  # How payment was made
    'iso_currency_code' # Currency type
]

"""
@dataclass
class Transaction():
    transaction_id: str
    access_token: str
    account_id: str
    amount: float
    date: date
    name: str
    merchant_name: str | None
    category: list[str] | None
    personal_finance_category: dict | None
    pending: bool
    payment_channel: str
    iso_currency_code: str

    def to_dict(self):
        # convert date to datetime for MongoDB storage
        datetime_obj = datetime.combine(self.date, datetime.min.time())
        
        return {
            'transaction_id': self.transaction_id,
            'access_token': self.access_token,
            'account_id': self.account_id,
            'amount': self.amount,
            'date': datetime_obj,  # Store as datetime
            'name': self.name,
            'merchant_name': self.merchant_name,
            'category': self.category,
            'personal_finance_category': self.personal_finance_category,
            'pending': self.pending,
            'payment_channel': self.payment_channel,
            'iso_currency_code': self.iso_currency_code
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        # handle date conversion from datetime if needed
        date_value = data['date']
        if isinstance(date_value, datetime):
            date_value = date_value.date()
            
        #apparently, the personal finance category is an object in itself, and if it has "to_dict" function, then we use THAT
        #to set the value of the personal finance categ. very weird.
        if hasattr(data.get('personal_finance_category', {}), 'to_dict'):
            personal_finance_cat = data['personal_finance_category'].to_dict()
        else: #in case this function does not exist, then it is not an object lol, so we can just get its value
            personal_finance_cat = data.get('personal_finance_category')

        return cls(
            transaction_id=data['transaction_id'],
            access_token=data['access_token'], 
            account_id=data['account_id'],
            amount=data['amount'],
            date=date_value,
            name=data['name'],
            merchant_name=data.get('merchant_name'),
            category=data.get('category'),
            personal_finance_category=personal_finance_cat,
            pending=data['pending'],
            payment_channel=data['payment_channel'],
            iso_currency_code=data['iso_currency_code']
        )


"""
general plan for schemas:

one collection for transactions, 

and another for cursors (not sure if more will need this), schema: 
cursor: string
access_token: string (this is to identify with a user)
cursor_type: "transactions"/something else if needed

"""

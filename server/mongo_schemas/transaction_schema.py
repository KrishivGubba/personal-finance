from dataclasses import dataclass, asdict
from datetime import date

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
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            transaction_id=data['transaction_id'],
            access_token=data['access_token'], 
            account_id=data['account_id'],
            amount=data['amount'],
            date=data['date'],
            name=data['name'],
            merchant_name=data['merchant_name'],
            category=data['category'],
            personal_finance_category=data['personal_finance_category'],
            pending=data['pending'],
            payment_channel=data['payment_channel'],
            iso_currency_code=data['iso_currency_code']
        )

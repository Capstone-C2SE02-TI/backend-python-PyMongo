from web3 import Web3
from dotenv import load_dotenv
import os
load_dotenv()

infura_key = os.environ['infura_key']

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_key}'))

new_transaction_filter = w3.eth.filter('pending')

print(new_transaction_filter.get_new_entries())




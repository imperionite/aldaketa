import os
from web3 import Web3
from dotenv import load_dotenv
import json

load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Load ABI
with open("contract_abi.json", "r") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Clear records
nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
tx = contract.functions.clearRecords().build_transaction({
    'from': ACCOUNT_ADDRESS,
    'nonce': nonce,
    'gas': 5000000, # increase gas limit to be able to clear the records as deleting is too expensive
    'gasPrice': w3.to_wei('20', 'gwei')
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"✅ All records cleared. Tx hash: {tx_hash.hex()}")

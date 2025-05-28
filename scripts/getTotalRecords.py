import os
from web3 import Web3
from dotenv import load_dotenv
import json

load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Connect to Web3
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Load ABI
with open("contract_abi.json", "r") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

try:
    total_records = contract.functions.getTotalRecords().call()
    print(f"📊 Total records stored: {total_records}")
except Exception as e:
    print(f"⚠️ Error fetching total records: {e}")

import os
from web3 import Web3
from dotenv import load_dotenv
import json
from datetime import datetime

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
    records = contract.functions.getAllRecords().call()
    if not records:
        print("ℹ️ No records found.")
    else:
        for i, record in enumerate(records):
            sensor_id, data_type, value, timestamp = record
            dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"📤 Record #{i + 1}: Sensor = {sensor_id}, Type = {data_type}, Value = {value}, Time = {dt}")
except Exception as e:
    print(f"⚠️ Error fetching records: {e}")

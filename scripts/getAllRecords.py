# scripts/getAllRecords.py (Milestone Week 6)

import os
import json
import pandas as pd
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Connect to Web3
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
assert w3.is_connected(), "❌ Web3 not connected"

# Load ABI
with open("contract_abi.json", "r") as f:
    abi = json.load(f)

# Load Contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Fetch all records
try:
    records = contract.functions.getAllRecords().call()

    if not records:
        print("ℹ️ No records found on the blockchain.")
        exit()

    # Convert to list of dicts for DataFrame
    data = []
    for r in records:
        sensor_id, data_type, value, timestamp = r
        data.append({
            "sensor_id": sensor_id,
            "data_type": data_type,
            "value": value,
            "timestamp": datetime.fromtimestamp(timestamp)  # Convert UNIX to datetime
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # Add numeric_value column (redundant here, but milestone requires it)
    df["numeric_value"] = pd.to_numeric(df["value"], errors="coerce")

    # Handle missing (if any)
    df.fillna(0, inplace=True)

    # Save cleaned CSV
    df.to_csv("cleaned_iot_data.csv", index=False)
    print("✅ Cleaned IoT data saved to cleaned_iot_data.csv")

    # Show preview
    print("\n📄 Cleaned Data Preview:")
    print(df.head())

except Exception as e:
    print(f"⚠️ Error retrieving records: {str(e)}")

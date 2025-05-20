import os
import pandas as pd
from web3 import Web3
from dotenv import load_dotenv
from utils import load_contract  # Ensure this is implemented
import time

# Load environment variables
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Load contract + Web3 instance
contract, w3 = load_contract(CONTRACT_ADDRESS)

# Load CSV data
df = pd.read_csv("synthetic_dataset.csv")

# Fields of interest
FIELDS = {
    "pH": "SENSOR_pH",
    "Temperature (°C)": "SENSOR_Temperature_°C",
    "Turbidity (NTU)": "SENSOR_Turbidity_NTU",
    "Conductivity (µS/cm)": "SENSOR_Conductivity_µS_cm",
    "ClO2 MS1 (mg/L)": "SENSOR_ClO2_mg_L"
}

# Interact with smart contract - ALL ROWS in the dataset will be stored
for idx, row in df.iterrows():
    for field, sensor_id in FIELDS.items():
        if pd.isnull(row[field]):
            continue  # Skip if no data

        value = int(float(row[field]))  # Cast to int (rounded)
        data_type = field
        timestamp = row["Timestamp"]  # for logging only

        try:
            nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

            tx = contract.functions.storeData(sensor_id, data_type, value).build_transaction({
                'from': ACCOUNT_ADDRESS,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': w3.to_wei('20', 'gwei')
            })

            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            print(f"📦 Stored {data_type}: {value} at {timestamp}")

            time.sleep(0.1)  # Optional: Avoid spamming too fast
        except Exception as e:
            print(f"⚠️ Failed to store {data_type} at row {idx}: {e}")

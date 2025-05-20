import os
import pandas as pd
from web3 import Web3
from dotenv import load_dotenv
from utils import load_contract
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

print("First 10 rows of the dataset:")
print(df.head(10))

# Fields of interest
FIELDS = {
    "pH": "SENSOR_pH",
    "Temperature (°C)": "SENSOR_Temperature_°C",
    "Turbidity (NTU)": "SENSOR_Turbidity_NTU",
    "Conductivity (µS/cm)": "SENSOR_Conductivity_µS_cm",
    "ClO2 MS1 (mg/L)": "SENSOR_ClO2_mg_L"
}

# Log file for tracking
log_file = open("iot_data_log.txt", "a")

# Interact with smart contract using batch method
for idx, row in df.head(10).iterrows():
    sensor_ids = []
    data_types = []
    values = []

    for field, sensor_id in FIELDS.items():
        raw_value = row[field]
        value = 0 if pd.isnull(raw_value) else int(float(raw_value))
        sensor_ids.append(sensor_id)
        data_types.append(field)
        values.append(value)

    try:
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

        tx = contract.functions.storeBatchData(sensor_ids, data_types, values).build_transaction({
            'from': ACCOUNT_ADDRESS,
            'nonce': nonce,
            'gasPrice': w3.to_wei('10', 'gwei'),
        })

        # Estimate gas for efficiency
        tx['gas'] = w3.eth.estimate_gas(tx)

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        log_entry = f"✅ Stored batch at {row['Timestamp']} | TX Hash: {tx_hash.hex()}"
        print(log_entry)
        log_file.write(log_entry + "\n")
        time.sleep(0.2)

    except Exception as e:
        error_msg = f"⚠️ Failed at row {idx} ({row['Timestamp']}): {str(e)}"
        print(error_msg)
        log_file.write(error_msg + "\n")

log_file.close()

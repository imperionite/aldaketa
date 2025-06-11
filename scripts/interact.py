import os
import pandas as pd
import time
from web3 import Web3
from dotenv import load_dotenv
from utils import load_contract

# Load environment variables
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Load contract + Web3 instance
contract, w3 = load_contract(CONTRACT_ADDRESS)

# Load full CSV
df = pd.read_csv("synthetic_dataset.csv")
print("✅ Loaded full dataset:", df.shape)

# Select 100 random rows
df_sample = df.sample(n=100, random_state=42).reset_index(drop=True)
print("🎲 Random sample selected. Preview:")
print(df_sample.head())

# Fields of interest
FIELDS = {
    "pH": "SENSOR_pH",
    "Temperature (°C)": "SENSOR_Temperature_°C",
    "Turbidity (NTU)": "SENSOR_Turbidity_NTU",
    "Conductivity (µS/cm)": "SENSOR_Conductivity_µS_cm",
    "ClO2 MS1 (mg/L)": "SENSOR_ClO2_mg_L"
}

# Log file
with open("iot_data_log.txt", "a") as log_file:
    for idx, row in df_sample.iterrows():
        for field, sensor_id in FIELDS.items():
            raw_value = row[field]
            if pd.isnull(raw_value):
                continue  # Skip if missing
            try:
                value = int(float(raw_value))
                nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

                tx = contract.functions.storeData(sensor_id, field, value).build_transaction({
                    'from': ACCOUNT_ADDRESS,
                    'nonce': nonce,
                    'gas': 200000,
                    'gasPrice': w3.to_wei('10', 'gwei')
                })

                signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                log_entry = f"✅ TX {tx_hash.hex()} | {sensor_id} | {field} | Value: {value} | Timestamp: {row['Timestamp']}"
                print(log_entry)
                log_file.write(log_entry + "\n")
                time.sleep(0.2)

            except Exception as e:
                error = f"⚠️ Error at row {idx}, {sensor_id}: {str(e)}"
                print(error)
                log_file.write(error + "\n")

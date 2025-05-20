import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")

# Setup Web3
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Install Solidity compiler
install_solc("0.8.0")

# Read Solidity source
with open("./contracts/IoTDataStorage.sol", "r") as file:
    contract_source = file.read()

# Compile Solidity contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "IoTDataStorage.sol": {
            "content": contract_source
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.0")

# Extract ABI and bytecode
abi = compiled_sol['contracts']['IoTDataStorage.sol']['IoTDataStorage']['abi']
bytecode = compiled_sol['contracts']['IoTDataStorage.sol']['IoTDataStorage']['evm']['bytecode']['object']

# Save ABI to contract_abi.json
with open("contract_abi.json", "w") as abi_file:
    json.dump(abi, abi_file)
    print("✅ ABI saved to contract_abi.json")

# Deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

tx = contract.constructor().build_transaction({
    'from': ACCOUNT_ADDRESS,
    'nonce': nonce,
    'gas': 3000000,
    'gasPrice': w3.to_wei('20', 'gwei')
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print(f"🚀 Contract deployed at: {contract_address}")

# Save contract address to .env
with open(".env", "a") as env_file:
    env_file.write(f"\nCONTRACT_ADDRESS={contract_address}\n")
    print("✅ CONTRACT_ADDRESS saved to .env")

import os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")

def load_contract(address):
    """Compile Solidity contract and connect to deployed instance"""

    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    
    if w3.is_connected():
        print("✅ Connected to Ganache successfully!")
    else:
        raise ConnectionError("❌ Web3 not connected. Check GANACHE_URL or Ganache status.")

    # Ensure Solidity version installed
    install_solc("0.8.0")

    # Read the smart contract source code
    with open("./contracts/IoTDataStorage.sol", "r") as file:
        source = file.read()

    # Compile contract
    compiled = compile_standard({
        "language": "Solidity",
        "sources": {
            "IoTDataStorage.sol": {"content": source}
        },
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi"]}
            }
        }
    }, solc_version="0.8.0")

    abi = compiled["contracts"]["IoTDataStorage.sol"]["IoTDataStorage"]["abi"]
    
    # Connect to deployed contract
    contract = w3.eth.contract(address=address, abi=abi)

    return contract, w3

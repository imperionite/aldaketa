import os
from web3 import Web3
from solcx import compile_standard
from dotenv import load_dotenv

load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")

def load_contract(address):
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    assert w3.is_connected(), "❌ Web3 not connected to Ganache"

    with open("./contracts/IoTDataStorage.sol", "r") as file:
        source = file.read()

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
    contract = w3.eth.contract(address=address, abi=abi)

    return contract, w3

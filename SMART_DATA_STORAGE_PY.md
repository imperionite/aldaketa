# aldaketa

Documentation for Homework: Smart Contract Data Storage (Python/Web3.py Implemetation)

## Steps

```sh
# 1. Install Ganache globally (yarn) and run on the terminal
ganache --deterministic # obtain the RPC ganache URL, one available acct and one private key, put it in .env
# 2. Run deploy.py to compile and deploy the Solidity smart contract with the Python script; contract_abi.json generated
python scripts/deploy.py
# 3. Connect to the deployed contract, store a few data points from your synthetic dataset CSV and optionally retrieve and display stored records
python scripts/interact.py # This will loop 5 environmental parameters in one row and sampled only the first 10 rows from the synthetic dataset
# Retrieve all recorded data points from the CSV
python scripts/retrieve_records.py
# clear all records
python scripts/clear_records.py # too expensive

```
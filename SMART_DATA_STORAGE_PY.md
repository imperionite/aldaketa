# aldaketa

Documentation for Homework: Smart Contract Data Storage (Python/Web3.py Implemetation)

## Steps

```sh
# 1. Install Ganache globally (yarn) and run on the terminal
# Obtain the RPC ganache URL (e.g. 127.0.0.1:8545), one available acct. (out of 10 given)and one private key (out of 10 given), put it in .env
# Account address must match the field # of private key
# CONTRACT_ADDRESS env. variable (generated automatically in .env file) anf contract_abi.json will automatically generated.
# 2. Place your solidity smart contract in contracts folder; other folder in the structure belongs to to Hardhat Nodejs implementation
$ ganache --deterministic 

# 3. Run deploy.py to compile and deploy the Solidity smart contract with the Python script; contract_abi.json generated
$ python scripts/deploy.py # This will also generate the CONTRACT_ADDRESS environment variable in .env; delete the old environment variable on the next run

# 4. Connect to the deployed contract, store a few data points from your synthetic dataset CSV and optionally retrieve and display stored records
$ python scripts/interact.py # This will loop 5 environmental parameters in one row and randomly sampled 100 rows from the synthetic dataset that will saved approx. 500 records but it will skip NAN values, so the resulting saved records accounting only < 500 records; # iot_data_log.txt will be generated

# 5. Retrieve all recorded data points from the CSV
$ python scripts/retrieve_records.py
$ python scripts/getTotalRecords.py

# 6. Retrieve all blockchain records using getAllRecords()
# Structure them into a Pandas DataFrame
# Convert timestamp into human-readable datetime
# Extract numeric values from the value field (though yours is already int, we’ll include it for completeness)
# Save cleaned data to cleaned_iot_data.csv for visualization
$ python scripts/getAllRecords.py

# clear all records
$ python scripts/clear_records.py # too expensive

# streamlit 
streamlit run streamlit_dashboard.py 

```
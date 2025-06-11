# Week 6 Homework: Data Retrieval and Processing

## 🌊 Water Quality Blockchain Ledger – Transaction Documentation

The water quality Blockchain Ledger development process involves multiple stages, including smart contract creation, deployment, data interaction, record retrieval, and management, all relying on Ethereum blockchain technology to ensure secure, transparent, and immutable logging of IoT sensor data.

This section serves as the documentation for the submitted homework pertaining to week 6, which emphasizes the functionality of data retrieval and processing within the blockchain ledger, as well as a summary of my MS 1 submission that transitions into MS 2. While the primary emphasis of this documentation is on data retrieval and processing, all functionalities coded within the smart contract I utilized are also presented to provide insight into my current standing in the ADET course.

### Smart Contract: `IoTDataStorage.sol`

The core of the system is the Smart Contract `IoTDataStorage`, written in Solidity 0.8.0, designed to store, retrieve, and manage water quality sensor data securely on-chain.

Check the smart contract that I used [here](https://github.com/imperionite/aldaketa/blob/main/contracts/IoTDataStorage.sol).

#### `storeData(sensorId, dataType, value)`

**Purpose**: Stores a single sensor reading on-chain.

**Inputs**:

- `sensorId (string)`: Unique ID of the IoT sensor (e.g., `"SENSOR_pH"`).
- `dataType (string)`: Type of data (e.g., `"pH"`).
- `value (int256)`: Measured value from the sensor.

**Behavior**:

- Validates non-empty `sensorId` and `dataType`.
- Captures `block.timestamp` as `timestamp`.
- Appends a `DataRecord` to `records`.
- Emits `DataStored` event.

**Event Emitted**:

```solidity
event DataStored(string sensorId, string dataType, int256 value, uint256 timestamp);
```

---

### `storeBatchData(sensorIds[], dataTypes[], values[])`

**Purpose**: Stores multiple sensor readings in one transaction (gas optimization). This function is already omitted from the regular transaction within this project.

**Inputs**:

- `sensorIds`: Array of sensor IDs.
- `dataTypes`: Array of data types.
- `values`: Array of values.

**Behavior**:

- Checks all input arrays are of the same length.
- Validates each input.
- Loops over arrays, storing each record with the same timestamp.
- Emits one `DataStored` event per record.

**Use Case**: Suitable for batch uploads (e.g., sensor gateways or synthetic testing).

---

### `getRecord(index)`

**Purpose**: Retrieves a single data record by its index. This function not fully implemented.

**Input**:

- `index (uint)`: Position in `records` array.

**Returns**:

- `(sensorId, dataType, value, timestamp)`

---

### `getAllRecords()`

**Purpose**: Returns all stored sensor data.

**Returns**:

- Array of `DataRecord` structs.

**Use Case**: Useful for dashboards, analytics tools, and full data export.

---

### `getTotalRecords()`

**Purpose**: Returns the total number of stored data records.

**Returns**:

- `uint` – total length of `records[]`.

---

### `clearRecords()`

**Purpose**: Deletes all stored records.

**Behavior**:

- Uses `delete records;` to remove all elements.

**Note**: This is **gas-expensive** due to the cost of clearing large storage arrays. Use cautiously.

---

## 🐍 Python Scripts – Transaction-Level Overview

---

### `deploy.py`

**Transaction**: Deploy Smart Contract
**Functionality**:

- Environment Setup: Uses .env to configure GANACHE_URL, PRIVATE_KEY, and ACCOUNT_ADDRESS for secure access to the Ethereum test network.
- Compiler Setup: Installs and uses Solidity compiler version 0.8.0 for contract compilation.
- Contract Compilation: Reads source, compiles to extract ABI and bytecode with detailed output selection for deployment.
- Deployment: Constructs a deployment transaction, signs it using the private key, and broadcasts it to the blockchain.
- Transaction Handling: Waits for transaction confirmation to obtain the deployed contract address.
- Persistence: Saves ABI to JSON and appends contract address to .env for easy reference by other scripts.
- Robust error and status logging guide users through deployment steps ensuring reliability.

**Outcome**:

- Deployed contract available at `CONTRACT_ADDRESS`.
- ABI saved to `contract_abi.json`.

![Deploy Transaction](https://drive.google.com/uc?id=1N7B8FcR5Z13t9UE3MKmv7jHbJ7z11NjL)

---

### `interact.py`

**Transaction**: Calls `storeData()` per record
**Data Source**: `synthetic_dataset.csv`
**Process**:

- Data Loading: Reads water quality readings from a synthetic_dataset.csv file into a pandas DataFrame and extracts a random sample of 100 entries for processing.
- Field Mapping: Maps standard water quality parameters (pH, temperature, turbidity, conductivity, chlorine dioxide) to corresponding sensor IDs used in smart contract calls.
- Transaction Building: For each sensor reading:

  - Builds `storeData()` transaction.
  - Prepares and signs transactions invoking the storeData function with sensor ID, data type, and integer value.
  - Logs the result in `iot_data_log.txt`.
  - Validates non-null numeric values.

- Transaction Execution: Sends signed transactions to the blockchain, awaits receipt, and logs transaction hashes with detailed metadata including sensor type and timestamp.
- Rate Limiting: Includes a short delay to avoid network congestion and nonce conflicts.
- Error Handling: Catches exceptions per record, logging errors with context for troubleshooting.

**Logged**:

```text
✅ TX <hash> | SENSOR_ID | DataType | Value | Timestamp
```

![Insert Records](https://drive.google.com/uc?id=1iB5geNlBFFU4h3xtWPQ4CAP5Qghn3lbL)

---

## Blockchain Data Retrieval

Two retrieval approaches provide comprehensive data auditing:

### `getAllRecords.py`

**Transaction**: Calls `getAllRecords()` (read-only)
**Process**:

- Connects to the blockchain and fetches the entire records array via getAllRecords.
- Converts UNIX timestamps to human-readable datetime formats.
- Stores cleaned and structured data into CSV for offline analysis. Saves to `cleaned_iot_data.csv`.
- Handles missing or corrupt data gracefully.
- Outputs previews for verification.

**Output**:

- CSV file with structured IoT sensor records.

![Get All Records](https://drive.google.com/uc?id=1d6CysDSSAwV3lKnPWDOoSd7yxe5y2JEU)

### `retrieve_records.py`

**Transaction**: Calls `getAllRecords()`
**Purpose**:

- Streams record-by-record to console with formatted display for quick inspection.
- Emphasizes transparency around sensor, data type, value, and timestamp.

**Format**:

```text
📤 Record #N: Sensor = SENSOR_ID, Type = DataType, Value = XX, Time = YYYY-MM-DD HH:MM:SS
```

![Retrieve Records](https://drive.google.com/uc?id=1d6CysDSSAwV3lKnPWDOoSd7yxe5y2JEU)

Both retrieval methods ensure immutable data transparency, supporting compliance and reporting.

---

### `getTotalRecords.py`

**Transaction**: Calls `getTotalRecords()`
**Purpose**:

- Retrieves and prints the number of total records stored.

**Output**:

```text
📊 Total records stored: <number>
```

## ![Get Total Records](https://drive.google.com/uc?id=1v32bdNFYM0ZwOUrLULYJy2y8DCzGeJqP)

### `clear_records.py`

**Transaction**: Calls `clearRecords()`
**Purpose**:

- Clears all data from the blockchain.

**Behavior**:

- Requires high gas limit (`10,000,000`) to succeed.
- Sends and logs the transaction hash after deletion.

**Caution**: Avoid using on Ethereum Mainnet unless necessary due to high gas cost.

![Clear Records](https://drive.google.com/uc?id=1YR7ksB_UjFif0rwW2-O-p2pX8fjeDR8b)

---

### Auxiliary Utility: `utils.py`

Offers a reusable function load_contract to:

- Connect Web3 to the configured network.
- Compile and extract ABI dynamically.
- Attach to the deployed contract instance.

**Helper Functions**:

- `load_contract(address)`: Compiles contract and connects to a deployed address.
- Ensures connection to Ganache and compiles ABI on the fly.
- Provides connectivity validation and error reporting to facilitate consistent interaction workflows.

---

## Notes on Gas Cost & Optimization

- **Single `storeData()`**:

  - \~20,000–40,000 gas per record depending on string length.

- **Batch `storeBatchData()`**:

  - \~100,000+ gas for 5 records.

- **Clear operation**:

  - **Very expensive** due to full array deletion.

- **Tip**: For Mainnet, store only hashes or aggregated data off-chain (e.g., via IPFS or Filecoin).

---

## Recommended Testing Flow

1. ✅ Deploy smart contract → `deploy.py`
2. 🔄 Insert records → `interact.py`
3. 📥 Retrieve and export data → `getAllRecords.py`
4. 🧹 Clear old data (optional) → `clear_records.py`

---

## 🧾 Event Emission (Logs)

Each data transaction emits:

```text
event DataStored(
    string sensorId,
    string dataType,
    int256 value,
    uint256 timestamp
);
```

# Week 6 Homework: Data Retrieval and Processing

## 🌊 Water Quality Blockchain Ledger – Transaction Documentation

A recap of my MS 1 submission and continuation leading to MS 2. 

### Smart Contract: `IoTDataStorage.sol`

Check the smart contract that I used [here](https://github.com/imperionite/aldaketa/blob/main/contracts/IoTDataStorage.sol).

#### `storeData(sensorId, dataType, value)`

**Purpose**: Stores a single sensor reading on-chain.

**Inputs**:

* `sensorId (string)`: Unique ID of the IoT sensor (e.g., `"SENSOR_pH"`).
* `dataType (string)`: Type of data (e.g., `"pH"`).
* `value (int256)`: Measured value from the sensor.

**Behavior**:

* Validates non-empty `sensorId` and `dataType`.
* Captures `block.timestamp` as `timestamp`.
* Appends a `DataRecord` to `records`.
* Emits `DataStored` event.

**Event Emitted**:

```solidity
event DataStored(string sensorId, string dataType, int256 value, uint256 timestamp);
```

---

### `storeBatchData(sensorIds[], dataTypes[], values[])`

**Purpose**: Stores multiple sensor readings in one transaction (gas optimization). This function is already omitted from the regular transaction within this project.

**Inputs**:

* `sensorIds`: Array of sensor IDs.
* `dataTypes`: Array of data types.
* `values`: Array of values.

**Behavior**:

* Checks all input arrays are of the same length.
* Validates each input.
* Loops over arrays, storing each record with the same timestamp.
* Emits one `DataStored` event per record.

**Use Case**: Suitable for batch uploads (e.g., sensor gateways or synthetic testing).

---

### `getRecord(index)`

**Purpose**: Retrieves a single data record by its index. This function not fully implemented.

**Input**:

* `index (uint)`: Position in `records` array.

**Returns**:

* `(sensorId, dataType, value, timestamp)`

---

### `getAllRecords()`

**Purpose**: Returns all stored sensor data.

**Returns**:

* Array of `DataRecord` structs.

**Use Case**: Useful for dashboards, analytics tools, and full data export.

---

### `getTotalRecords()`

**Purpose**: Returns the total number of stored data records.

**Returns**:

* `uint` – total length of `records[]`.

---

### `clearRecords()`

**Purpose**: Deletes all stored records.

**Behavior**:

* Uses `delete records;` to remove all elements.

**Note**: This is **gas-expensive** due to the cost of clearing large storage arrays. Use cautiously.

---

## 🐍 Python Scripts – Transaction-Level Overview

---

### `deploy.py`

**Transaction**: Deploy Smart Contract
**Functionality**:

* Compiles the Solidity contract.
* Builds and signs a deployment transaction.
* Sends it to the blockchain.
* Waits for and logs the contract address.

**Outcome**:

* Deployed contract available at `CONTRACT_ADDRESS`.
* ABI saved to `contract_abi.json`.

![Deploy Transaction](https://drive.google.com/uc?id=1N7B8FcR5Z13t9UE3MKmv7jHbJ7z11NjL)

---

### `interact.py`

**Transaction**: Calls `storeData()` per record
**Data Source**: `synthetic_dataset.csv`
**Process**:

* Reads CSV, samples 100 rows.
* Extracts and cleans data from columns (e.g., pH, Turbidity).
* For each reading:

  * Builds `storeData()` transaction.
  * Signs and sends it.
  * Logs the result in `iot_data_log.txt`.

**Logged**:

```text
✅ TX <hash> | SENSOR_ID | DataType | Value | Timestamp
```

![Insert Records](https://drive.google.com/uc?id=1iB5geNlBFFU4h3xtWPQ4CAP5Qghn3lbL)

---

### `getAllRecords.py`

**Transaction**: Calls `getAllRecords()` (read-only)
**Process**:

* Fetches all records.
* Converts to pandas DataFrame.
* Converts timestamps to readable format.
* Saves to `cleaned_iot_data.csv`.

**Output**:

* CSV file with structured IoT sensor records.

![Get All Records](https://drive.google.com/uc?id=1d6CysDSSAwV3lKnPWDOoSd7yxe5y2JEU)

---

### `retrieve_records.py`

**Transaction**: Calls `getAllRecords()`
**Purpose**:

* Prints each record to the terminal for inspection.

**Format**:

```text
📤 Record #N: Sensor = SENSOR_ID, Type = DataType, Value = XX, Time = YYYY-MM-DD HH:MM:SS
```

![Retrieve Records](https://drive.google.com/uc?id=1d6CysDSSAwV3lKnPWDOoSd7yxe5y2JEU)
---

### `getTotalRecords.py`

**Transaction**: Calls `getTotalRecords()`
**Purpose**:

* Retrieves and prints the number of total records stored.

**Output**:

```text
📊 Total records stored: <number>
```

![Get Total Records](https://drive.google.com/uc?id=1v32bdNFYM0ZwOUrLULYJy2y8DCzGeJqP)
---

### `clear_records.py`

**Transaction**: Calls `clearRecords()`
**Purpose**:

* Clears all data from the blockchain.

**Behavior**:

* Requires high gas limit (`10,000,000`) to succeed.
* Sends and logs the transaction hash after deletion.

**Caution**: Avoid using on Ethereum Mainnet unless necessary due to high gas cost.

![Clear Records](https://drive.google.com/uc?id=1YR7ksB_UjFif0rwW2-O-p2pX8fjeDR8b)

---

### `utils.py`

**Helper Functions**:

* `load_contract(address)`: Compiles contract and connects to a deployed address.
* Ensures connection to Ganache and compiles ABI on the fly.

---

## Notes on Gas Cost & Optimization

* **Single `storeData()`**:

  * \~20,000–40,000 gas per record depending on string length.
* **Batch `storeBatchData()`**:

  * \~100,000+ gas for 5 records.
* **Clear operation**:

  * **Very expensive** due to full array deletion.
* **Tip**: For Mainnet, store only hashes or aggregated data off-chain (e.g., via IPFS or Filecoin).

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


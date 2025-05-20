# aldaketa

This project focuses on simulating environmental sensor data for smart monitoring systems in the context of water quality monitoring as critical monitoring system for public health and environmental sustainability. Water supply networks are vulnerable to contamination, and timely detection of anomalies is essential for safe drinking water. Modern water systems use IoT sensors to collect high-frequency data (e.g., every minute) from various points in the distribution network.

The GECCO Industrial Challenges ([2018](https://www.spotseven.de/wp-content/uploads/2018/03/rulesGeccoIc2018.pdf) & [2019](https://www.th-koeln.de/mam/downloads/deutsch/hochschule/fakultaeten/informatik_und_ingenieurwissenschaften/rulesgeccoic2019.pdf)) provide real-world datasets and problem settings for developing and benchmarking algorithms for online anomaly/event/change detection in water quality time series. The datasets from GECCo 2018-2019 are harmonized, concatenated and processed to create a unified synthetic dataset for this project.

The project involves creating a synthetic dataset that mimics real sensor data measurements used in water plants, and prepares the data for future use in a blockchain-based system for secure, decentralized record-keeping.

## Reference

Moritz, S., Rehbach, F., Chandrasekaran, S., Rebolledo, M., & Thomas Bartz-Beielstein. (2018). GECCO Industrial Challenge 2018 Dataset: A water quality dataset for the 'Internet of Things: Online Anomaly Detection for Drinking Water Quality' competition at the Genetic and Evolutionary Computation Conference 2018, Kyoto, Japan. [Data set]. The Genetic and Evolutionary Computation Conference (GECCO), Kyoto, Japan. Zenodo. [https://doi.org/10.5281/zenodo.3884398](https://doi.org/10.5281/zenodo.3884398)


Moritz, S., Rehbach, F., & Bartz-Beielstein, T. (2019). GECCO Industrial Challenge 2019 Dataset: A water quality dataset for the 'Internet of Things: Online Event Detection for Drinking Water Quality Control' competition at the Genetic and Evolutionary Computation Conference 2019, Prague, Czech Republic. [Data set]. The Genetic and Evolutionary Computation Conference (GECCO), Prague, Czech Republic. Zenodo. [https://doi.org/10.5281/zenodo.4304080](https://doi.org/10.5281/zenodo.4304080)

### Sample Solidity Smart Contract Based on Homework: Smart Contract Data Storage

```solidity

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IoTDataStorage {
    struct DataRecord {
        string sensorId;      // e.g., SENSOR_Temperature
        string dataType;      // e.g., Temperature (°C)
        int256 value;         // Numeric value, defaults to 0 if missing
        uint256 timestamp;    // Unix timestamp of when data is stored
    }

    DataRecord[] public records;

    event DataStored(string sensorId, string dataType, int256 value, uint256 timestamp);

    // Store a new data point with input validation
    function storeData(string memory sensorId, string memory dataType, int256 value) public {
        require(bytes(sensorId).length > 0, "Sensor ID cannot be empty");
        require(bytes(dataType).length > 0, "Data type cannot be empty");
        // Optional: Add domain-specific value checks if needed
        // e.g., require(value >= -100 && value <= 100, "Value out of expected range");

        uint256 currentTime = block.timestamp;

        records.push(DataRecord({
            sensorId: sensorId,
            dataType: dataType,
            value: value,
            timestamp: currentTime
        }));

        emit DataStored(sensorId, dataType, value, currentTime);
    }

    // Retrieve a record by index with bounds checking
    function getRecord(uint index) public view returns (string memory, string memory, int256, uint256) {
        require(index < records.length, "Index out of range");
        DataRecord memory record = records[index];
        return (record.sensorId, record.dataType, record.value, record.timestamp);
    }

    // Get total number of stored records
    function getTotalRecords() public view returns (uint) {
        return records.length;
    }
}

```
The code uses standard practices for input validation and data storage. It also follows best practices by using require statements for basic checks (e.g., non-empty sensor ID) and emits events for logging purposes, which can be useful in monitoring the contract's activity without compromising its integrity.
Suggestion: However, as with any smart contract deployment, it is crucial to audit this code thoroughly before deploying it on a live network. Additionally, consider implementing more comprehensive security measures such as using secure randomness (if applicable), protecting against denial-of-service attacks through appropriate gas limits or rate limiting mechanisms, and ensuring that the data stored does not become a privacy concern if compromised. Deploying any smart contract should be done with caution after thorough review by experienced developers to ensure it aligns with your project's security requirements.
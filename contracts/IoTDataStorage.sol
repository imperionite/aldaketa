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
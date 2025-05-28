// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IoTDataStorage {
    struct DataRecord {
        string sensorId;
        string dataType;
        int256 value;
        uint256 timestamp;
    }

    DataRecord[] public records;

    event DataStored(
        string sensorId,
        string dataType,
        int256 value,
        uint256 timestamp
    );

    // Store a new data point with input validation
    function storeData(
        string memory sensorId,
        string memory dataType,
        int256 value
    ) public {
        require(bytes(sensorId).length > 0, "Sensor ID cannot be empty");
        require(bytes(dataType).length > 0, "Data type cannot be empty");

        uint256 currentTime = block.timestamp;

        records.push(
            DataRecord({
                sensorId: sensorId,
                dataType: dataType,
                value: value,
                timestamp: currentTime
            })
        );

        emit DataStored(sensorId, dataType, value, currentTime);
    }

    // Retrieve a record by index
    function getRecord(
        uint index
    ) public view returns (string memory, string memory, int256, uint256) {
        require(index < records.length, "Index out of range");
        DataRecord memory record = records[index];
        return (
            record.sensorId,
            record.dataType,
            record.value,
            record.timestamp
        );
    }

    // Get total number of stored records
    function getTotalRecords() public view returns (uint) {
        return records.length;
    }

    // Clear all records
    function clearRecords() public {
        delete records;
    }

    // Retrieve all records
    function getAllRecords() public view returns (DataRecord[] memory) {
        return records;
    }

    /* ##################################
    
    function storeBatchData() is to reduce gas by storing multiple sensor readings in one call; Minimize on-chain cost by batching data
    This implementation though ealistic, is only applicable for prototyping and automatic sensor push
    On Ethereum Mainnet:
    Storing 256 bits (32 bytes) costs roughly 20,000 gas
    1 gas ~ 20–100 gwei → $0.01 to $0.50+ per entry
    The batch storeBatchData() with 5 sensors = ~100,000+ gas
    → Not sustainable at scale

    It is also Likely handle the synthetic dataset implemeted more efficiently.
    #######################################
    */
    function storeBatchData(
        string[] memory sensorIds,
        string[] memory dataTypes,
        int256[] memory values
    ) public {
        require(
            sensorIds.length == dataTypes.length &&
                dataTypes.length == values.length,
            "Input array lengths mismatch"
        );

        uint256 currentTime = block.timestamp;

        for (uint256 i = 0; i < sensorIds.length; i++) {
            require(bytes(sensorIds[i]).length > 0, "Sensor ID empty");
            require(bytes(dataTypes[i]).length > 0, "Data type empty");

            records.push(
                DataRecord({
                    sensorId: sensorIds[i],
                    dataType: dataTypes[i],
                    value: values[i],
                    timestamp: currentTime
                })
            );

            emit DataStored(sensorIds[i], dataTypes[i], values[i], currentTime);
        }
    }
}

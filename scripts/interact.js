const hre = require("hardhat");

async function main() {
  const contractAddress = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0";
  const IoTDataStorage = await hre.ethers.getContractAt("IoTDataStorage", contractAddress);

  // Store example data (optional)
 // const tx = await IoTDataStorage.storeData("SENSOR_Temperature_°C", "Temperature (°C)", 7);
  const tx = await IoTDataStorage.storeData("SENSOR_Conductivity_µS_cm", "Conductivity (µS/cm)", 198);
  await tx.wait();
  console.log("📦 Data stored!");

  // Get total number of records
  const total = await IoTDataStorage.getTotalRecords();
  console.log(`📊 Total Records: ${total}`);

  // Retrieve and print all records
  for (let i = 0; i < total; i++) {
    const record = await IoTDataStorage.getRecord(i);
    console.log(`📤 Record #${i}:`, {
      sensorId: record[0],
      dataType: record[1],
      value: record[2].toString(),
      timestamp: new Date(Number(record[3]) * 1000).toLocaleString()
    });
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

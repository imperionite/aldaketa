const hre = require("hardhat");

async function main() {
  const contractAddress = "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9"; // manually paste the contract address deployed
  const IoTDataStorage = await hre.ethers.getContractAt("IoTDataStorage", contractAddress);

  // Store example data (optional)
  // use the extracting_sample_data for the format based on IoTDataStorage.sol validation
  // 1. const tx = await IoTDataStorage.storeData("SENSOR_Temperature_°C", "Temperature (°C)", 7); // take note of the format as the input is validated
  // 2. const tx = await IoTDataStorage.storeData("SENSOR_Conductivity_µS_cm", "Conductivity (µS/cm)", 198); // take note of the format as the input is validated
  // 3. const tx = await IoTDataStorage.storeData("SENSOR_Turbidity_NTU", "Turbidity (NTU)", 0); // take note of the format as the input is validated
  // 4. const tx = await IoTDataStorage.storeData("SENSOR_ClO2_mg_L", "ClO2 (mg/L)", 0); // take note of the format as the input is validated
  const tx = await IoTDataStorage.storeData("SENSOR_pH", "pH", 8); // take note of the format as the input is validated
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


const hre = require("hardhat");

async function main() {
  const IoTDataStorage = await hre.ethers.getContractFactory("IoTDataStorage");
  const contract = await IoTDataStorage.deploy();
  await contract.waitForDeployment();
  console.log(`✅ Contract deployed to: ${await contract.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

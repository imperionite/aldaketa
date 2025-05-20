# aldaketa

Documentation for Homework: Smart Contract Data Storage

## Steps

Ensure that Ganache package is installed globally.

```sh
# 1. For NodeJS version, initialize Node project
npm init -y
npm i -D hardhat
npx hardhat init # create JS project & install packages that will be prompted
npm i ethers dotenv # maybe optional for now

# 2. Structure the Solidity smart contract in contracts/ generated IoTDataStorage.sol
# 3. Compile the smart contract
npx hardhat compile # Sample output: Compiled 1 Solidity file successfully (evm target: paris).
# 4. Create and deploy the deployment script under scripts/deploy.js
npx hardhat node
# on another terminal; 
npx hardhat run scripts/deploy.js --network localhost #Sample output: ✅ Contract deployed to: 0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9

# 5. After deploying the smart contract, interact using Hardhat 
npx hardhat run scripts/interact.js --network localhost


# 5. Start Ganache (separate terminal)
ganache

```
import Web3 from "web3";
import { newKitFromWeb3, CeloContract } from "@celo/contractkit";
import 'dotenv/config';
const web3 = new Web3("https://forno.celo.org");
const kit = newKitFromWeb3(web3);
import * as fs from "node:fs";
const secret_path = process.env.SECRET_PATH;

const contractAddress = process.env.CONTRACT_ADDRESS;
if (!web3.utils.isAddress(contractAddress)) {
    throw new Error("Invalid Ethereum address from environment variables");
}

const myAddress = process.env.MY_ADDRESS;
if (!web3.utils.isAddress(myAddress)) {
    throw new Error("Invalid Ethereum address from environment variables");
}

function createAccount_contract_kit() {
    console.log('Creating a new account')
    const account = web3.eth.accounts.create();
    console.log(`Made new account ${account.address}`)
    fs.writeFileSync(secret_path, account.privateKey)
    console.log(`Account private key saved to ${secret_path}`)
}

function getAccount_contract_kit() {
    console.log('Getting your account')
    if (!fs.existsSync(secret_path)) {
        console.log('No account found, create one first')
        return false
    }

    const privateKey = fs.readFileSync(secret_path, 'utf8');
    const account = web3.eth.accounts.privateKeyToAccount(privateKey);
    console.log(`Found account ${account.address}`)
    return account
}

async function main() {
    console.log('Celo interactions with ContractKit');
    console.log('Creating account');
    createAccount_contract_kit();
    getAccount_contract_kit();

    console.log("Using preset address of:", myAddress);

    let totalBalance = await kit.getTotalBalance(myAddress);
    console.log(`Preset account has a total balance for ${myAddress}:`, totalBalance);

    console.log("Celo interactions with thirdweb SDK");


}

(async () => {
    try {
        await main();
        console.log('Finished execution');
    } catch (error) {
        console.error('Error running the main function', error);
    }
})();

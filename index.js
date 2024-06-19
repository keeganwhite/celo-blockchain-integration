import Web3 from "web3";
import { newKitFromWeb3, CeloContract } from "@celo/contractkit";
import 'dotenv/config';

const web3 = new Web3("https://forno.celo.org");
const kit = newKitFromWeb3(web3);

// Ensure the address is valid
const myAddress = process.env.MY_ADDRESS;
if (!web3.utils.isAddress(myAddress)) {
    throw new Error("Invalid Ethereum address from environment variables");
}

async function main() {
    console.log("Using address:", myAddress);

    let totalBalance = await kit.getTotalBalance(myAddress);
    console.log(`Total balance for ${myAddress}:`, totalBalance);

}

(async () => {
    try {
        await main();
        console.log('Finished execution');
    } catch (error) {
        console.error('Error running the main function', error);
    }
})();

import Web3 from "web3";
import { newKitFromWeb3, CeloContract } from "@celo/contractkit";
import 'dotenv/config';
const web3 = new Web3("https://alfajores-forno.celo-testnet.org");
const kit = newKitFromWeb3(web3);
const myAddress = process.env.MY_ADDRESS;
// Main async function to run your application logic
async function main() {
    console.log("Starting the application...");

    let accounts = await kit.web3.eth.getAccounts();
    kit.defaultAccount = accounts[0];
    // paid gas in cUSD
    await kit.setFeeCurrency(CeloContract.StableToken);

    let totalBalance = await kit.getTotalBalance(myAddress);
    console.log(`Total balance for ${myAddress}:`, totalBalance);
    console.log("Operation completed successfully.");
}


(async () => {
    try {
        await main();
        console.log('Finished execution');
    } catch (error) {
        console.error('Error running the main function', error);
    }
})();

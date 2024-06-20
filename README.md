# celo-blockchain-integration

Code in Javascript and Python to create an eth wallet, load the Krone Contract* (erc-20 token) and transact between
wallets*. Find Krone [here](https://celoscan.io/token/0x8bab657c88eb3c724486d113e650d2c659aa23d2).

_*note: this is only implemented in Python_

Replace the ABI json file with whatever other contract you want use and update the contract address if you want to try 
another token.

## Pre-requisites
Ensure you create .env files as per the  .env.example files

### Run JavaScript
1. `cd js`
2. `npm install`
3. `npm start`

### Run Python
1. `cd py`
2. `pip install -r requirements.txt`
3. `python3 main.py`
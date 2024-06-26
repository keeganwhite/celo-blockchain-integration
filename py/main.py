from web3 import Web3
from dotenv import load_dotenv
import os
import json

def create_account(w3):
    account = w3.eth.account.create()
    print(f"New account created: {account.address}")
    print(f"Private key: {account._private_key.hex()}")
    return account

def load_contract_abi(file_path):
    with open(file_path, 'r') as abi_file:
        return json.load(abi_file)


def check_balance_ether(w3, address):
    balance = w3.eth.get_balance(address)
    eth_balance = w3.from_wei(balance, 'ether')
    return eth_balance


def check_balance_custom_contract(contract, address):
    raw_balance = contract.functions.balanceOf(address).call()
    token_decimals = contract.functions.decimals().call()
    # Adjust the balance based on the token decimals
    adjusted_balance = raw_balance / (10 ** token_decimals)
    return adjusted_balance


def get_token_name(contract):
    name = contract.functions.name().call()
    return name


def get_token_symbol(contract):
    symbol = contract.functions.symbol().call()
    return symbol


def estimate_gas_for_transfer(contract, from_address, to_address, amount):
    # Prepare the transaction for gas estimation
    decimals = contract.functions.decimals().call()
    token_amount = int(amount * (10 ** decimals))

    # Estimating gas
    gas_estimate = contract.functions.transfer(to_address, token_amount).estimate_gas({
        'from': from_address  # Sender's address
    })
    print(f"Estimated gas for transfer: {gas_estimate}")
    return gas_estimate


def send_token(w3, chain_id, contract, from_address, to_address, amount, private_key):
    # Calculate the token amount adjusted for decimals
    decimals = contract.functions.decimals().call()
    token_amount = int(amount * (10 ** decimals))
    gas = estimate_gas_for_transfer(contract, from_address, to_address, amount)

    # Fetch the current network gas price
    current_gas_price = w3.eth.gas_price
    print(f"Current network gas price: {current_gas_price} wei")

    # Prepare the transaction
    nonce = w3.eth.get_transaction_count(from_address)
    tx = contract.functions.transfer(to_address, token_amount).build_transaction({
        'chainId': chain_id,  # Celo's chain ID
        'gas': gas,
        'gasPrice': current_gas_price,
        'nonce': nonce,
    })

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Transaction sent! Hash:", tx_hash.hex())

    # Wait for the transaction to be mined
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


def main():
    load_dotenv()
    private_key = os.getenv('PRIVATE_KEY')
    sender_address = os.getenv('SENDER_ADDRESS')
    recipient_address = os.getenv('RECIPIENT_ADDRESS')
    contract_address = os.getenv('CONTRACT_ADDRESS')
    if not (private_key and sender_address and recipient_address and contract_address):
        print('ERROR reading in environment variables. Check .env exists and is populated as per .env.example')
        exit(1)
    w3 = Web3(Web3.HTTPProvider('https://forno.celo.org'))
    network_id = w3.net.version
    print(f"Connected to network with ID: {network_id}")
    chain_id = w3.eth.chain_id
    print("Chain ID:", chain_id)
    contract_abi = load_contract_abi('contract_abi.json')
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    token_name = get_token_name(contract)
    token_symbol = get_token_symbol(contract)

    print(f'Analysing {token_name} accounts')

    sender_balance = check_balance_custom_contract(contract, sender_address)
    print(f'Account {sender_address} has a {sender_balance} {token_symbol}')

    recipient_balance = check_balance_custom_contract(contract, recipient_address)
    print(f'Account {recipient_address} has a {recipient_balance} {token_symbol}')

    print(f'Sending {token_symbol}')
    receipt = send_token(w3, chain_id, contract, sender_address, recipient_address, 1, private_key)
    print("Transaction receipt:", receipt)

    print('Fetching new balances...')
    sender_balance = check_balance_custom_contract(contract, sender_address)
    print(f'Account {sender_address} has a {sender_balance} {token_symbol}')

    recipient_balance = check_balance_custom_contract(contract, recipient_address)
    print(f'Account {recipient_address} has a {recipient_balance} {token_symbol}')


if __name__ == '__main__':
    main()

from web3 import Web3
from dotenv import load_dotenv
import os


def create_account(w3):
    account = w3.eth.account.create()
    print(f"New account created: {account.address}")
    print(f"Private key: {account._private_key.hex()}")
    return account


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
    contract_abi = [{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint8","name":"_decimals","type":"uint8"},{"internalType":"int128","name":"_decayLevel","type":"int128"},{"internalType":"uint256","name":"_periodMinutes","type":"uint256"},{"internalType":"address","name":"_defaultSinkAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_owner","type":"address"},{"indexed":True,"internalType":"address","name":"_spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_burner","type":"address"},{"indexed":False,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"_oldCap","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_newCap","type":"uint256"}],"name":"Cap","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"int128","name":"_foo","type":"int128"},{"indexed":True,"internalType":"uint256","name":"_bar","type":"uint256"}],"name":"Debug","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"_period","type":"uint256"},{"indexed":True,"internalType":"uint256","name":"_periodCount","type":"uint256"},{"indexed":True,"internalType":"int128","name":"_oldAmount","type":"int128"},{"indexed":False,"internalType":"int128","name":"_newAmount","type":"int128"}],"name":"Decayed","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_timestamp","type":"uint256"}],"name":"Expired","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"_oldTimestamp","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_newTimestamp","type":"uint256"}],"name":"ExpiryChange","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_minter","type":"address"},{"indexed":True,"internalType":"address","name":"_beneficiary","type":"address"},{"indexed":False,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_period","type":"uint256"}],"name":"Period","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_account","type":"address"},{"indexed":True,"internalType":"uint256","name":"_period","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Redistribution","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bool","name":"_final","type":"bool"},{"indexed":False,"internalType":"uint256","name":"_sealState","type":"uint256"}],"name":"SealStateChange","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_from","type":"address"},{"indexed":True,"internalType":"address","name":"_to","type":"address"},{"indexed":False,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"actualPeriod","outputs":[{"internalType":"uint128","name":"","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_minter","type":"address"}],"name":"addWriter","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"applyDemurrage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_rounds","type":"uint256"}],"name":"applyDemurrageLimited","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"applyExpiry","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"baseBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"changePeriod","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"uint256","name":"_period","type":"uint256"}],"name":"decayBy","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decayLevel","outputs":[{"internalType":"int128","name":"","type":"int128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_minter","type":"address"}],"name":"deleteWriter","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"demurrageAmount","outputs":[{"internalType":"int128","name":"","type":"int128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_target","type":"uint256"}],"name":"demurrageCycles","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"demurrageTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"expires","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_supply","type":"uint256"},{"internalType":"int128","name":"_demurrageAmount","type":"int128"}],"name":"getDistribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"period","type":"uint32"},{"internalType":"uint72","name":"value","type":"uint72"},{"internalType":"uint64","name":"demurrage","type":"uint64"}],"internalType":"struct DemurrageTokenSingleNocap.redistributionItem","name":"_redistribution","type":"tuple"}],"name":"getDistributionFromRedistribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"_lastTimestamp","type":"uint256"}],"name":"getMinutesDelta","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_periodCount","type":"uint256"}],"name":"getPeriodTimeDelta","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"period","type":"uint32"},{"internalType":"uint72","name":"value","type":"uint72"},{"internalType":"uint64","name":"demurrage","type":"uint64"}],"internalType":"struct DemurrageTokenSingleNocap.redistributionItem","name":"_redistribution","type":"tuple"}],"name":"isEmptyRedistribution","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"_state","type":"uint256"}],"name":"isSealed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_minter","type":"address"}],"name":"isWriter","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSealState","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mintTo","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"periodDuration","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"periodStart","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"redistributionCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"redistributions","outputs":[{"internalType":"uint32","name":"period","type":"uint32"},{"internalType":"uint72","name":"value","type":"uint72"},{"internalType":"uint64","name":"demurrage","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_state","type":"uint256"}],"name":"seal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sealState","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_expirePeriod","type":"uint256"}],"name":"setExpirePeriod","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_cap","type":"uint256"}],"name":"setMaxSupply","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_sinkAddress","type":"address"}],"name":"setSinkAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sinkAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"_sum","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"sweep","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"toBaseAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_participants","type":"uint256"},{"internalType":"int128","name":"_demurrageModifier","type":"int128"},{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"uint256","name":"_period","type":"uint256"}],"name":"toRedistribution","outputs":[{"components":[{"internalType":"uint32","name":"period","type":"uint32"},{"internalType":"uint72","name":"value","type":"uint72"},{"internalType":"uint64","name":"demurrage","type":"uint64"}],"internalType":"struct DemurrageTokenSingleNocap.redistributionItem","name":"","type":"tuple"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"period","type":"uint32"},{"internalType":"uint72","name":"value","type":"uint72"},{"internalType":"uint64","name":"demurrage","type":"uint64"}],"internalType":"struct DemurrageTokenSingleNocap.redistributionItem","name":"_redistribution","type":"tuple"}],"name":"toRedistributionDemurrageModifier","outputs":[{"internalType":"int128","name":"","type":"int128"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"period","type":"uint32"},{"internalType":"uint72","name":"value","type":"uint72"},{"internalType":"uint64","name":"demurrage","type":"uint64"}],"internalType":"struct DemurrageTokenSingleNocap.redistributionItem","name":"_redistribution","type":"tuple"}],"name":"toRedistributionPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"uint32","name":"period","type":"uint32"},{"internalType":"uint72","name":"value","type":"uint72"},{"internalType":"uint64","name":"demurrage","type":"uint64"}],"internalType":"struct DemurrageTokenSingleNocap.redistributionItem","name":"_redistribution","type":"tuple"}],"name":"toRedistributionSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalBurned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalMinted","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSink","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]
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

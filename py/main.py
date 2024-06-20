from web3 import Web3


def main():
    w3 = Web3(Web3.HTTPProvider('https://forno.celo.org'))
    network_id = w3.net.version
    print(f"Connected to network with ID: {network_id}")

if __name__ == '__main__':
    main()
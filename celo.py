from web3 import Web3
import requests
from typing import List, Dict
import time
from datetime import datetime

class CeloExplorer:
    def __init__(self):
        # Network RPC endpoints
        self.networks = {
            'mainnet': {
                'rpc': 'https://forno.celo.org',
                'explorer_api': 'https://api.celoscan.io/api',
                'name': 'Celo Mainnet'
            },
            'alfajores': {
                'rpc': 'https://alfajores-forno.celo-testnet.org',
                'explorer_api': 'https://api-alfajores.celoscan.io/api',
                'name': 'Celo Alfajores Testnet'
            }
        }

        # You'll need to replace this with your CeloScan API key
        self.api_key = 'PXFHGHMZPWURFH6EPJ39RGG93A1565HSNE'

    def get_contract_deployments(self, address: str, network: str) -> List[Dict]:
        """
        Query all smart contracts deployed by a specific address on the specified network.

        Args:
            address (str): The address to query
            network (str): Network to query ('mainnet' or 'alfajores')

        Returns:
            List[Dict]: List of deployed contracts with their details
        """
        if network not in self.networks:
            raise ValueError(f"Invalid network. Choose from: {list(self.networks.keys())}")

        network_config = self.networks[network]

        # Create API URL
        api_url = (f"{network_config['explorer_api']}?"
                  f"module=account&action=txlist&address={address}&"
                  f"apikey={self.api_key}")

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if data['status'] != '1':
                print(f"Error: {data['message']}")
                return []

            # Filter for contract creation transactions
            contract_deployments = []
            for tx in data['result']:
                if tx['to'] == '':  # Empty 'to' field indicates contract creation
                    contract_info = {
                        'contract_address': tx['contractAddress'],
                        'transaction_hash': tx['hash'],
                        'block_number': int(tx['blockNumber']),
                        'timestamp': datetime.fromtimestamp(int(tx['timeStamp'])),
                        'gas_used': int(tx['gasUsed']),
                        'status': 'Success' if tx['isError'] == '0' else 'Failed'
                    }
                    contract_deployments.append(contract_info)

            return contract_deployments

        except requests.exceptions.RequestException as e:
            print(f"Error querying {network_config['name']}: {str(e)}")
            return []

    def get_contract_details(self, contract_address: str, network: str) -> Dict:
        """
        Get additional details about a deployed contract.

        Args:
            contract_address (str): The contract address to query
            network (str): Network to query ('mainnet' or 'alfajores')

        Returns:
            Dict: Contract details including verification status and other metadata
        """
        network_config = self.networks[network]
        api_url = (f"{network_config['explorer_api']}?"
                  f"module=contract&action=getabi&address={contract_address}&"
                  f"apikey={self.api_key}")

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            contract_details = {
                'address': contract_address,
                'verified': data['status'] == '1',
                'abi': data['result'] if data['status'] == '1' else None
            }

            return contract_details

        except requests.exceptions.RequestException as e:
            print(f"Error getting contract details: {str(e)}")
            return None

def main():
    # Example usage
    explorer = CeloExplorer()
    address_to_query = '0xE23a4c6615669526Ab58E9c37088bee4eD2b2dEE'  # Replace with the address you want to query

    for network in ['mainnet', 'alfajores']:
        print(f"\nQuerying {explorer.networks[network]['name']}...")

        # Get all contract deployments
        deployments = explorer.get_contract_deployments(address_to_query, network)

        if not deployments:
            print(f"No contracts found on {network}")
            continue

        print(f"\nFound {len(deployments)} contract deployments:")
        for deployment in deployments:
            print("\nContract Details:")
            print(f"Address: {deployment['contract_address']}")
            print(f"Deployed at: {deployment['timestamp']}")
            print(f"Status: {deployment['status']}")

            # Get additional contract details
            details = explorer.get_contract_details(deployment['contract_address'], network)
            if details:
                print(f"Verified: {'Yes' if details['verified'] else 'No'}")

            print("-" * 50)

        # Add delay to avoid rate limiting
        time.sleep(1)

if __name__ == "__main__":
    main()
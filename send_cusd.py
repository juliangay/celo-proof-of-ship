from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Celo network (using Forno RPC)
w3 = Web3(Web3.HTTPProvider('https://alfajores-forno.celo-testnet.org'))

# cUSD contract address on Celo mainnet
# CUSD_CONTRACT_ADDRESS = '0x765DE816845861e75A25fCA122bb6898B8B1282a'

# cUSD contract address on Celo Alfajores testnet
CUSD_CONTRACT_ADDRESS = '0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1'

# Your wallet private key (never share this!)
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

SAFE_ADDRESS = os.getenv("SAFE_ADDRESS")  # Replace with your Safe wallet address: CELO ALFAJORES


RECIPIENT_ADDRESS = os.getenv("RECIPIENT_ADDRESS")

# Standard ERC20 ABI for cUSD
ERC20_ABI = json.loads('''[
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]''')

def send_cusd(private_key, to_address, amount_cusd):
    # Create account object from private key
    account = Account.from_key(private_key)
    
    # Get contract instance
    cusd_contract = w3.eth.contract(
        address=CUSD_CONTRACT_ADDRESS,
        abi=ERC20_ABI
    )
    
    # Convert 1 cUSD to wei (cUSD has 18 decimals)
    amount_wei = w3.to_wei(amount_cusd, 'ether')
    
    # Build transaction
    transaction = cusd_contract.functions.transfer(
        to_address,
        amount_wei
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 100000,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt



# Safe contract ABI (minimal version for demonstration)
SAFE_ABI = json.loads('''[
    {
        "inputs": [
            {"type": "address", "name": "to"},
            {"type": "uint256", "name": "value"},
            {"type": "bytes", "name": "data"},
            {"type": "uint8", "name": "operation"},
            {"type": "uint256", "name": "safeTxGas"},
            {"type": "uint256", "name": "baseGas"},
            {"type": "uint256", "name": "gasPrice"},
            {"type": "address", "name": "gasToken"},
            {"type": "address", "name": "refundReceiver"},
            {"type": "bytes", "name": "signatures"}
        ],
        "name": "execTransaction",
        "outputs": [{"type": "bool", "name": "success"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]''')

# Standard ERC20 ABI for cUSD (transfer function)
ERC20_ABI = json.loads('''[
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]''')

def send_cusd_from_safe(owner_private_key, to_address, amount_cusd):
    # Create account object from private key
    owner_account = Account.from_key(owner_private_key)
    
    # Get contract instances
    safe_contract = w3.eth.contract(address=SAFE_ADDRESS, abi=SAFE_ABI)
    cusd_contract = w3.eth.contract(address=CUSD_CONTRACT_ADDRESS, abi=ERC20_ABI)
    
    # Convert amount to wei
    amount_wei = w3.to_wei(amount_cusd, 'ether')
    
    # Create the transfer data
    transfer_data = cusd_contract.functions.transfer(
        to_address, 
        amount_wei
    ).build_transaction({
        'from': owner_account.address,
        'nonce': 0,  # Nonce doesn't matter for getting data
        'gas': 0,    # Gas doesn't matter for getting data
        'gasPrice': 0  # Gas price doesn't matter for getting data
    })['data']
    
    # Create Safe transaction parameters
    safe_tx_params = {
        'to': CUSD_CONTRACT_ADDRESS,
        'value': 0,
        'data': transfer_data,
        'operation': 0,  # CALL operation
        'safeTxGas': 0,
        'baseGas': 0,
        'gasPrice': 0,
        'gasToken': '0x0000000000000000000000000000000000000000',
        'refundReceiver': '0x0000000000000000000000000000000000000000',
        'signatures': b''  # This would need to be populated with required signatures
    }
    
    # Build and execute Safe transaction
    transaction = safe_contract.functions.execTransaction(
        safe_tx_params['to'],
        safe_tx_params['value'],
        safe_tx_params['data'],
        safe_tx_params['operation'],
        safe_tx_params['safeTxGas'],
        safe_tx_params['baseGas'],
        safe_tx_params['gasPrice'],
        safe_tx_params['gasToken'],
        safe_tx_params['refundReceiver'],
        safe_tx_params['signatures']
    ).build_transaction({
        'from': owner_account.address,
        'nonce': w3.eth.get_transaction_count(owner_account.address),
        'gas': 500000,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, owner_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt



if __name__ == "__main__":
    # Replace these with your actual values
    AMOUNT_CUSD = 1.0  # Amount in cUSD
    
    try:
        # receipt = send_cusd(PRIVATE_KEY, RECIPIENT_ADDRESS, AMOUNT_CUSD)
        receipt = send_cusd_from_safe(PRIVATE_KEY, RECIPIENT_ADDRESS, AMOUNT_CUSD)
        print(f"Transaction successful! Transaction hash: {receipt['transactionHash'].hex()}")
    except Exception as e:
        print(f"Error: {e}")



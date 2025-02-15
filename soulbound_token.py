from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv
from solcx import compile_source
from datetime import datetime

# Load environment variables
load_dotenv()

# Alfajores testnet RPC URL
ALFAJORES_RPC_URL = "https://alfajores-forno.celo-testnet.org"

# Connect to Celo network
w3 = Web3(Web3.HTTPProvider(ALFAJORES_RPC_URL))

# Your wallet private key (never share this!)
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

RECIPIENT_ADDRESS = os.getenv("RECIPIENT_ADDRESS")

# Simplified Solidity source code without OpenZeppelin
SOLIDITY_SOURCE = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleSoulboundToken {
    // Token name and symbol
    string public name = "SimpleSoulboundToken";
    string public symbol = "SBT";
    
    // Token ID counter
    uint256 private _tokenIdCounter;
    
    // Contract owner
    address public owner;
    
    // Mapping from token ID to owner address
    mapping(uint256 => address) private _owners;
    
    // Mapping from token ID to token URI
    mapping(uint256 => string) private _tokenURIs;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }
    
    function mint(address to, string memory uri) public onlyOwner returns (uint256) {
        require(to != address(0), "Invalid recipient");
        
        _tokenIdCounter++;
        uint256 newTokenId = _tokenIdCounter;
        
        _owners[newTokenId] = to;
        _tokenURIs[newTokenId] = uri;
        
        emit Transfer(address(0), to, newTokenId);
        
        return newTokenId;
    }
    
    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "Token doesn't exist");
        return owner;
    }
    
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        require(_owners[tokenId] != address(0), "Token doesn't exist");
        return _tokenURIs[tokenId];
    }
    
    // Prevent transfers - makes the token soulbound
    function transfer(address, uint256) public pure {
        revert("Tokens are soulbound and cannot be transferred");
    }
    
    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
}
'''

def compile_contract():
    """Compile the Solidity contract and return the ABI and bytecode."""
    compiled_sol = compile_source(
        SOLIDITY_SOURCE,
        output_values=['abi', 'bin'],
        solc_version='0.8.0'
    )
    contract_interface = compiled_sol['<stdin>:SimpleSoulboundToken']
    return contract_interface['abi'], contract_interface['bin']

def deploy_soulbound_token():
    # Get contract ABI and bytecode
    abi, bytecode = compile_contract()
    
    # Create account object
    account = Account.from_key(PRIVATE_KEY)
    
    # Create contract object
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Build constructor transaction
    construct_txn = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 1000000,  # Reduced gas since contract is simpler
        'gasPrice': w3.eth.gas_price,
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(construct_txn, PRIVATE_KEY)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt.contractAddress, abi

def mint_soulbound_token(contract_address, abi, recipient, token_uri):
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    # Get the latest nonce with pending transactions included
    nonce = w3.eth.get_transaction_count(recipient, 'pending')
    
    # Build the transaction
    mint_txn = contract.functions.mint(recipient, token_uri).build_transaction({
        'from': recipient,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign and send the transaction
    signed_txn = w3.eth.account.sign_transaction(mint_txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    return w3.eth.wait_for_transaction_receipt(tx_hash)


def upload_to_web3_storage(metadata):
    headers = {
        'Authorization': f'Bearer {YOUR_WEB3_STORAGE_TOKEN}'  # Get from web3.storage
    }
    
    files = {
        'file': ('metadata.json', json.dumps(metadata))
    }
    
    response = requests.post(
        'https://api.web3.storage/upload',
        headers=headers,
        files=files
    )
    
    return response.json()['cid']



def main():
    # Deploy the contract
    print("Deploying contract...")
    contract_address, abi = deploy_soulbound_token()
    print(f"Contract deployed at: {contract_address}")
    
    # Example recipient address
    recipient = RECIPIENT_ADDRESS
    
    # Example token URI (IPFS or other metadata location)
    token_uri = "ipfs://YOUR_METADATA_CID"
    
    # Mint token
    tx_receipt = mint_soulbound_token(contract_address, abi, recipient, token_uri)
    print(f"Token minted! Transaction hash: {tx_receipt.transactionHash.hex()}")
    print(f"See on Celoscan: https://alfajores.celoscan.io/tx/0x{tx_receipt.transactionHash.hex()}")

if __name__ == "__main__":
    main()

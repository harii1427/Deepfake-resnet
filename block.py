import gradio as gr
from web3 import Web3
import base64
import numpy as np


alchemy_provider = "https://eth-sepolia.g.alchemy.com/v2/257GmA3dnUQTEG5jeDLYAvkGXOyBdGry"
web3 = Web3(Web3.HTTPProvider(alchemy_provider))

# Define your contract ABI and address here
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "uploader",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "mediaType",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "hashValue",
                "type": "string"
            }
        ],
        "name": "MultimediaVerified",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "mediaType",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "hashValue",
                "type": "string"
            }
        ],
        "name": "uploadMultimedia",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "name": "multimediaHashes",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "mediaType",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "hashValue",
                "type": "string"
            }
        ],
        "name": "verifyMultimedia",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
contract_address = "0xC73d42561CD3b7257fF214386fcFDDf0109501Cb"
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
private_key = "e5b8ffed1f59a51f3f83a099c86dbe73b84c0220e9416227a09ad0228028e9a1"
account = web3.eth.account.from_key(private_key).address

def encode_base64(file_data):
    if isinstance(file_data, np.ndarray):
        # Convert ndarray to bytes and then encode as base64
        encoded_data = base64.b64encode(file_data.tobytes()).decode('utf-8')
    else:
        # Assume file_path is a string representing the file path
        with open(file_data, "rb") as file:
            encoded_data = base64.b64encode(file.read()).decode('utf-8')
    return encoded_data

def upload_to_blockchain(media_type, hash_value):
    private_key = "e5b8ffed1f59a51f3f83a099c86dbe73b84c0220e9416227a09ad0228028e9a1"
    account = web3.eth.account.from_key(private_key).address
    nonce = web3.eth.get_transaction_count(account)
    tx = contract.functions.uploadMultimedia(media_type, hash_value).build_transaction({
        'chainId': 11155111,
        'gas': 3000000,
        'gasPrice': Web3.to_wei(10, 'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

def blockchain_upload_interface(input_data):
    # Assume input_data contains the path to the media file
    media_path = input_data
    media_type = "video"  # Adjust as needed
    hash_value = encode_base64(media_path)
    tx_hash = upload_to_blockchain(media_type, hash_value)
    return f"File uploaded to blockchain with transaction hash: {tx_hash}"

blockchain_interface = gr.Interface(
    fn=blockchain_upload_interface,
    inputs=gr.File(label="Upload File"),
    outputs="text",
    title="Blockchain Media Upload",
    description="Upload media file to blockchain"
)

if __name__ == '__main__':
    blockchain_interface.launch()

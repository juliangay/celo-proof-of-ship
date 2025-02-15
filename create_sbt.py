import requests
import json
import os
from dotenv import load_dotenv

def download_image(url, filename):
    """Download image from URL"""
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

def upload_to_web3_storage(file_path):
    """Upload file to web3.storage and return CID"""
    # Get API token from environment variable
    WEB3_STORAGE_TOKEN = os.getenv('WEB3_STORAGE_TOKEN')
    
    headers = {
        'Authorization': f'Bearer {WEB3_STORAGE_TOKEN}'
    }
    
    with open(file_path, 'rb') as f:
        files = {
            'file': f
        }
        response = requests.post(
            'https://api.web3.storage/upload',
            headers=headers,
            files=files
        )
        
        return response.json()['cid']

def main():
    # Download Celo logo
    image_url = "https://images.ctfassets.net/wr0no19kwov9/5yVbTScDuXaZE0JL0w1kL0/f626c00085927069b473e684148c36f3/Union_1_.svg"
    image_filename = "celo_logo.svg"
    download_image(image_url, image_filename)
    
    # Upload image to IPFS
    image_cid = upload_to_web3_storage(image_filename)
    image_uri = f"ipfs://{image_cid}"
    print(f"Image uploaded to IPFS: {image_uri}")
    
    # Create metadata with IPFS image
    metadata = {
        "name": "Celo Proof of Ship",
        "description": "This token represents completion of a Celo Proof of Ship milestone",
        "image": image_uri,
        "attributes": [
            {
                "trait_type": "Achievement",
                "value": "Celo Proof of Ship milestone"
            },
            {
                "trait_type": "Date",
                "value": "2024"
            }
        ]
    }
    
    # Save metadata to file
    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
    
    # Upload metadata to IPFS
    metadata_cid = upload_to_web3_storage('metadata.json')
    metadata_uri = f"ipfs://{metadata_cid}"
    print(f"Metadata uploaded to IPFS: {metadata_uri}")
    
    # Clean up local files
    os.remove(image_filename)
    os.remove('metadata.json')
    
    return metadata_uri

if __name__ == "__main__":
    load_dotenv()
    metadata_uri = main()
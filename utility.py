import uuid
import json
from datetime import datetime
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import time

def generate_unique_id():
    unique_id = uuid.uuid4()
    return str(unique_id)

def get_date():
    timestamp_value = datetime.now()
    return timestamp_value

def sign_transaction(data, private_key):
    

    # Calculate hash for the serialized data
    hash_value = SHA256.new(json.dumps(data).encode('utf-8'))

    signature = pkcs1_15.new(private_key).sign(hash_value)
    return signature




def transmit_transaction(data, signature, public_key):
    
    
    # Convert data and signature to JSON format
    transaction_data = json.dumps(data)
    signature_data = signature.hex()
    public_key_data = public_key.export_key().decode('utf-8')

    # Create JSON payload
    payload = {
        "transaction_data": transaction_data,
        "signature": signature_data,
        "public_key": public_key_data
    }

    # Simulate sending payload to RSU
    print("Transmitting transaction data to RSU...")
    print(json.dumps(payload, indent=4))
    print("Transmission complete.")

def generateKeys():
    # Generate RSA key pair
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    return private_key, public_key
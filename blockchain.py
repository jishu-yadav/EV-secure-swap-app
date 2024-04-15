from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from datetime import datetime
import json

class ElectricVehicle:
    def __init__(self, identity):
        self.identity = identity
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

    def sign_data(self, data):
        hash_value = SHA256.new(data.encode('utf-8'))
        signature = pkcs1_15.new(self.private_key).sign(hash_value)
        return signature

    def transmit_transaction_details(self, transaction_details, rsu_public_key):
       
        transaction_details_list = list(transaction_details)

        # Adding timestamp to transaction details
        transaction_details_list.append(str(datetime.now()))

        # Convert back to tuple
        transaction_details = tuple(transaction_details_list)
       
        
        
        # Serialize transaction details
        serialized_data = json.dumps(transaction_details)       

        # Signing transaction details
        signature = self.sign_data(serialized_data)     

        # Transmitting data, hash, and signature to RSU
        return serialized_data, signature

class RoadSideUnit:
    def __init__(self, public_key):
        self.public_key = public_key

    def verify_transaction(self, serialized_data, signature):
        try:
            # Deserializing transaction details
            transaction_details = json.loads(serialized_data)

            # Verifying the integrity of the data
            hash_value = SHA256.new(serialized_data.encode('utf-8'))
            pkcs1_15.new(self.public_key).verify(hash_value, signature)

            # Printing after Successfully verified
            print("Data integrity verified.")
            return transaction_details
        except (ValueError, TypeError):
            print("Data integrity verification failed.")
            return None

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, block):
        self.chain.append(block)



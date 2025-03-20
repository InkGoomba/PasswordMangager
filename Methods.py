import customtkinter as ctk
import json
from cryptography.fernet import Fernet

# Generate a key and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

# Load the key from the file
def load_key():
    with open('filekey.key', 'rb') as filekey:
        return filekey.read()

# Encrypt a JSON file
def encrypt_json(input_file, output_file, key):
    fernet = Fernet(key)
    with open(input_file, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(output_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Decrypt a JSON file
def decrypt_json(input_file, output_file, key):
    fernet = Fernet(key)
    with open(input_file, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(output_file, 'wb') as dec_file:
        dec_file.write(decrypted)
    return json.loads(decrypted.decode('utf-8'))

# Loads key from flash drive
def load_key_from_flash_drive(flash_drive_path):
    try:
        with open(flash_drive_path, 'rb') as filekey:
            return filekey.read()
    except FileNotFoundError:
        print("Key file not found on the flash drive. Please ensure the flash drive is connected and the path is correct.")
        return None

# Example usage
generate_key()
key = load_key()
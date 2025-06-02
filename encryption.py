import os
from cryptography.fernet import Fernet

KEY_PATH = "keys/secret.key"

def generate_key():
    if not os.path.exists("keys"):
        os.makedirs("keys")
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    return open(KEY_PATH, "rb").read()

def encrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)

    with open(filepath, "rb") as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(filepath, "wb") as file:
        file.write(encrypted)

def decrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)

    with open(filepath, "rb") as file:
        encrypted = file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(filepath, "wb") as file:
        file.write(decrypted)


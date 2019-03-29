from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Crypto.Cipher import AES
import pyAesCrypt

def store_privKey(private_key):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb') as f:
        f.write(pem)

def store_pubKey(public_key):
    pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
    with open('public_key.pem', 'wb') as f:
        f.write(pem)

def genKey():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend= default_backend()
    )
    return private_key

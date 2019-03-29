from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Crypto.Cipher import AES
import pyAesCrypt
import Keys
import os
import random


#Generate an RSA private key
private_key = Keys.genRSAKey()
#Generate a RSA public key
public_key = private_key.public_key()

#Generate AES key and encrypte file
bufferSize = 64 * 1024
key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
pyAesCrypt.encryptFile("data.txt", "data.txt.aes", key, bufferSize)

#encode the string into a byte for RSA
byteKey = key.encode('utf-8')

#Encrypt the AES key with RSA
encryptedAESKey = Keys.encryptRSA(byteKey, public_key)

#Decrypt the AES key with RSA
decryptedAESKey = Keys.decryptRSA(encryptedAESKey, private_key)

#Byte to string to decode the file
decKey = decryptedAESKey.decode('utf-8')
#Decrypt file
pyAesCrypt.decryptFile("data.txt.aes", "dataout.txt", decKey, bufferSize)

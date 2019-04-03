from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def store_privKey(private_key):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb+') as f:
        f.write(pem)

def store_pubKey(public_key):
    pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
    pem1 = pem.decode()
    return pem1
#    server = [pem1]
#    with open("public_keys.txt","w+") as f: #in write mode
#        f.write("{}".format(server))
#    pkIdentifier = ''
#    for x in range(400, 425):
#        pkIdentifier += pem1[x]
#    return pkIdentifier

def readKey():
    with open("public_keys.txt") as f: #in read mode, not in write mode, careful
        rd=f.readlines()
    return rd

def keyToBytes(public_key):
    pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
    return pem

def genRSAKey():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend= default_backend()
    )
    return private_key

def encryptRSA(byteKey, public_key):
    #Encrypt RSA
    encryptedKey = public_key.encrypt(
        byteKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encryptedKey
#decrypt RSA
def decryptRSA(encryptedAESKey, private_key):
    original_message = private_key.decrypt(
        encryptedAESKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message

def findKey(file, identifier):
    y = 0
    count = len(file)
    start = 400
    pkLength = 434
    while (y != count):
        pKey = file[y]
        toCompare = ''
        for x in range (start, pkLength):
            toCompare += pKey[x]
        y = y + 1
        start = start + 464
        pkLength = pkLength + 464

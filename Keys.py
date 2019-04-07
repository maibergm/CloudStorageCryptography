from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from pydrive.auth import GoogleAuth
import quickstart
import hashlib

def authenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
    file1.SetContentString('Hello World!') # Set content of the file from given string.
    file1.Upload()


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
def AESKey():
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    key = hashlib.sha256(iv).digest()
    return key
    
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

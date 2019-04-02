from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from flask import Flask, render_template, request
import os
import random
import string
import Keys
import json

server = Flask(__name__)
PORT = 8080
@server.route("/")
def index():
    return render_template('index.html')

@server.route("/userCreate", methods =['POST'])
def createAUser():
    username = request.form.get('username')
    N = 6
    groupCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    private_key = Keys.genRSAKey()
    Keys.store_privKey(private_key)
    public_key = private_key.public_key()
    Keys.store_pubKey(public_key, username)
    return render_template('userCreate.html', groupCode = groupCode, username = username)

if __name__ == "__main__":
    server.run(port=PORT)

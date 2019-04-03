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
import mysql.connector

server = Flask(__name__)
PORT = 8080

@server.route("/")
def index():
    return render_template('index.html')

@server.route("/userCreate", methods =['POST'])
def createAUser():
    groups = dict()
    N = 6
    username = request.form.get('username') #get the username that the user gave
    groupCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) #generate a random string for the room id
    private_key = Keys.genRSAKey() # Generate a private key
    Keys.store_privKey(private_key) # Store the private key locally
    public_key = private_key.public_key() # Create a public key
    identifier = Keys.store_pubKey(public_key) #Store the public key and get an identifier for it
    server = {username:identifier} # match the user with the private key
    groups[groupCode] = [username] # Create a group code room and put the creator in it
    return render_template('userCreate.html', groupCode = groupCode, username = username)

@server.route("/joinGroup", methods =['POST'])
def joinAGroup():
    return render_template()
if __name__ == "__main__":
    server.run(port=PORT)

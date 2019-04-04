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
import sqlite3
import pymongo

server = Flask(__name__)
PORT = 8080
@server.route("/")
def index():
    return render_template('index.html')

@server.route("/creator", methods =['POST'])
def createAUser():
    groups = dict()
    N = 6
    username = request.form.get('username') #get the username that the user gave
    groupCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) #generate a random string for the room id
    private_key = Keys.genRSAKey() # Generate a private key
    Keys.store_privKey(private_key) # Store the private key locally
    public_key = private_key.public_key() # Create a public key
    pKey = Keys.store_pubKey(public_key) #Get the public key
    groups = {groupCode:[username]}
    users = {username:pKey}
    with open("groups.json", "a+") as write_file:
        json.dump(groups, write_file)
    with open("users.json", "w+") as write_file:
        json.dump(users, write_file)
    return render_template('creator.html', groupCode = groupCode, username = username)

@server.route("/member", methods =['POST'])
def joinAGroup():
    roomID = request.form.get('roomID')
    username = request.form.get('username')
    with open("groups.json") as read_file:
      groupLoad = json.loads(read_file)

    private_key = Keys.genRSAKey()
    Keys.store_privKey(private_key)
    public_key = private_key.public_key()
    pKey = Keys.store_pubKey(public_key)
    users = {username:pKey}

    return render_template('member.html')
if __name__ == "__main__":
    server.run(port=PORT)

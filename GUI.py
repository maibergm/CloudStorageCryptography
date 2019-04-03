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
myclient = pymongo.MongoClient("mongodb+srv://maxmai96:hello123@encryptionserver-2tccp.gcp.mongodb.net/test?retryWrites=true")

mydb = myclient["server"]
mycol = mydb["users"]

myList = {'sAdfS7':['Max', 'Dima', 'George']}
x = mycol.insert_one(myList)

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
    pKey = Keys.store_pubKey(public_key) #Store the public key and get an identifier for it
    users = [username, 'Dima', 'Dan']
    usersDump = json.dumps(users)
#    server = {username:identifier} # match the user with the private key
#    groups[groupCode] = [username] # Create a group code room and put the creator in it
    conn = sqlite3.connect('server.sqlite')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, public_key) VALUES (?, ?)',
          (username, pKey))
    cur.execute('INSERT INTO groups (groupCode, users) VALUES (?, ?)',
          (groupCode, usersDump))
    conn.commit()
    conn.close()
    return render_template('creator.html', groupCode = groupCode, username = username)

@server.route("/member", methods =['POST'])
def joinAGroup():
    roomID = request.form.get('roomID')
    conn = sqlite3.connect('server.sqlite')
    curr = conn.cursor()
    curr.execute('SELECT users FROM groups WHERE groupCode = "%s"' % (roomID))
    data = curr.fetchall()
    conn.close()

    return render_template('member.html')
if __name__ == "__main__":
    server.run(port=PORT)

from flask import Flask, render_template, request

server = Flask(__name__)
PORT = 8080
@server.route("/")
def index():
    return "hello world"
if __name__ == "__main__":
    server.run(port=PORT)

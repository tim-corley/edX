from flask import Flask

# create/define new application using flask, __name__ = representing this file is going to be the web app
app = Flask(__name__)

@app.route("/")
# when going to default route (/), run following function
def index():
    return "Hello, world!"

@app.route("/jim")
def jim():
    return "Hello, James!"

@app.route("/<string:name>")
def hello(name):
    name = name.capitalize()
    text = "Hello, " + name
    return text

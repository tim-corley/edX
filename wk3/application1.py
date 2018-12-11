import datetime

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    headline = "Hello, World! Welcome & Enjoy."
    return render_template("index0.html", headline=headline)

@app.route("/bye")
def bye():
    headline = "Goodbye! Please Stop By Again."
    return render_template("index0.html", headline=headline)

@app.route("/mybirthday")
def birthday():
    now = datetime.datetime.now()
    my_birthday = now.month == 02 and now.day == 15
    return render_template("index1.html", my_birthday=my_birthday)

@app.route("/names")
def show_names():
    names = ["Mac", "Dennis", "Dee", "Charlie", "Frank"]
    return render_template("index2.html", names=names)

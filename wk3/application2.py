from flask import Flask, render_template, request, session
# unable to get this working, see: https://stackoverflow.com/questions/51313324/modulenotfounderror-no-module-named-flask-session
from flask_session import Session
# from flask_session.__init__ import Session
# from flask.ext.session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

notes = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")
        notes.append(note)

    return render_template("index3.html", notes=notes)

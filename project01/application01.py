import os, requests
from models import db
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from flask_session import Session
# from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# Bootstrap(app)

GR_KEY = os.environ.get('GOODREADS_KEY')
POSTGRES = os.environ.get('DATABASE_URL')
SESSION_KEY = os.getenv('PROJECT01_SECRET')

app.config['DEBUG'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ('POSTGRES')
app.secret_key = ('SESSION_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
engine = create_engine(POSTGRES)
db.init_app(app)

@app.route("/")
def main():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello There!"

@app.route('/login', methods=['POST'])

def admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('incorrect password.')
    return main()

@app.route('/logout')

def logout():
    session['logged_in'] = False
    return main()

if __name__ == "__main__":
    main()

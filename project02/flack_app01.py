import os
from flask import Flask, session, render_template, request, redirect, url_for, g
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if g.user:
        return render_template('index.html', name=g.user)

    if request.method == 'POST':
        session.pop('user', None)
        session['user'] = request.form['username']
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/index', methods=['GET'])
def index():
    if g.user:
        return render_template('index.html', name=g.user)

    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

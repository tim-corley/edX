import os, requests
from models import *
from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, jsonify
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

GR_KEY = os.environ.get('GOODREADS_KEY')
POSTGRES = os.environ.get('DATABASE_URL')
SESSION_KEY = os.getenv('PROJECT01_SECRET')

app.config['DEBUG'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = ('SESSION_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
engine = create_engine(POSTGRES)
db.init_app(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])

class BookSearchForm(FlaskForm):
    choices = [('ISBN', 'ISBN'),
               ('Title', 'Title'),
               ('Author', 'Author'),
               ('Year', 'Year')]
    select = SelectField('Search for book:', choices=choices)
    search = StringField('', validators=[InputRequired(), Length(min=4, max=80)])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('search'))

        return '<h1>Invalid Username or Password.</h1>'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('search'))

    return render_template('register.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search = BookSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('search.html', form=search, name=current_user.username)

@app.route('/results', methods=['POST'])
@login_required
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db_session.query(title)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('search')
    else:
        # display results
        return render_template('results.html', results=results)

@app.route('/splash')
@login_required
def splash():
    return render_template('splash.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    main()

import os, requests, json
from models import *
from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, jsonify
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
migrate = Migrate(app, db)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

GR_KEY = os.environ.get('GOODREADS_KEY')
POSTGRES = os.environ.get('DATABASE_URL')
SESSION_KEY = os.getenv('PROJECT01_SECRET')

app.config['DEBUG'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = ('SESSION_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)
engine = create_engine(POSTGRES)
db = scoped_session(sessionmaker(bind=engine))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])

class BookSearchForm(FlaskForm):
    search = StringField('Search Term', validators=[InputRequired(), Length(min=4, max=80)])

class BookReviewForm(FlaskForm):
    new_review = StringField('Review', validators=[InputRequired(), Length(min=4, max=400)])

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
        db.add(new_user)
        db.commit()

        if check_password_hash(new_user.password, form.password.data):
            login_user(new_user)
            return redirect(url_for('search'))

    return render_template('register.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = BookSearchForm()

    if form.validate_on_submit():
        text = form.search.data
        results = db.execute(
            "SELECT * FROM books WHERE (LOWER(isbn) LIKE LOWER(:text)) OR (LOWER(title) LIKE LOWER(:text)) OR (author LIKE LOWER(:text)) LIMIT 20",
            { "text": '%' + text + '%'}
        ).fetchall()
        return render_template('search.html', form=form, results=results, name=current_user.username)
    return render_template('search.html', form=form, name=current_user.username)

@app.route("/books")
@login_required
def books():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=books)

@app.route('/details/<int:book_id>', methods=['GET', 'POST'])
@login_required
def details(book_id):
    # Make sure book exists
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book exists here.")

    book_id = book.id
    ISBN = book.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GR_KEY, "isbns": ISBN})
    data = res.json()
    rating = data['books'][0]['average_rating']

    # TODO switch these to raw SQL commands as per spec
    book = Books.query.get(book_id)
    reviews = Reviews.query.filter_by(book_id=book_id).all()

    form = BookReviewForm()

    if form.validate_on_submit():
        new_review = form.new_review.data
        book.add_review(new_review)
        return redirect(url_for('thanks'))

    return render_template("details.html", form=form, book=book, rating=rating, reviews=reviews)

# create an endpoint
@app.route('/api/<isbn>')
def book_api(isbn):
    # Make sure book exists
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {'isbn': isbn}).fetchone()
    if book is None:
        return jsonify({'error': 'Invalid ISBN'}), 422

    # Get review info
    ISBN = book.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GR_KEY, "isbns": ISBN})
    data = res.json()
    average_rating = data['books'][0]['average_rating']
    reviews_count = data['books'][0]['reviews_count']
    return jsonify({
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'isbn': book.isbn,
        'eviews_count': reviews_count,
        'average_rating': average_rating
    })

@app.route('/thanks', methods=['GET', 'POST'])
@login_required
def thanks():
    return render_template('thanks.html', name=current_user.username)

@app.route('/splash')
@login_required
def splash():
    return render_template('splash.html', name=current_user.username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    main()

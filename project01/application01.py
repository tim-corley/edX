import os
import requests
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

KEY = os.environ.get('GOODREADS_KEY')
POSTGRES = os.environ.get('DATABASE_URL')
engine = create_engine(POSTGRES)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")

def main():
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": "9781632168146"})
    if res.status_code != 200:
        raise Exception('ERROR: API request unsuccessful.')
    data = res.json()
    return jsonify(data)

if __name__ == "__main__":
    main()

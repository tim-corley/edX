import csv
import os
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI_2')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    # open and read the flights file
    f = open('flights01.csv')
    reader = csv.reader(f)
    # loop over each line in the file
    for origin, destination, duration, in reader:
        # create new flight object
        flight = Flight(origin=origin, destination=destination, duration=duration)
        # equivelent to INSERT, will add flight to db
        db.session.add(flight)
        print(f'added flight from {origin} to {destination}')
    # actually update the db with new data
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()

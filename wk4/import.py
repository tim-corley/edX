import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('SQLALCHEMY_DATABASE_URI')
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("flights.csv")
    reader = csv.reader(f)
    for origin, destination, duration, in reader:
        db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :desination, :duration)",
            {"origin": origin, "desination": destination, "duration": duration})
        print(f'Added flight from {origin} to {destination}')
    db.commit()

if __name__ == "__main__":
    main()

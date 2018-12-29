import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

POSTGRES = os.getenv('DATABASE_URL')
engine = create_engine(POSTGRES)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    # skip the header
    next(reader, None)
    for isbn, title, author, year, in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isbn, "title": title, "author": author, "year":year})
    db.commit()
    print('Added book details to table')

if __name__ == "__main__":
    main()

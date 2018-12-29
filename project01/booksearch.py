import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

POSTGRES = os.getenv('DATABASE_URL')
engine = create_engine(POSTGRES)
db = scoped_session(sessionmaker(bind=engine))

def main():

    # prompt user to choose a ISBN
    isbn = str(input("\nISBN: "))
    details = db.execute("SELECT title, author, year FROM books WHERE isbn = :isbn",
                        {"isbn": isbn}).fetchall()

    # make sure isbn is valid
    if not details:
        print('No such ISBN available')
    else:
        print('\nBook:')
        for detail in details:
            print(detail.title + ' By: ' + detail.author)

if __name__ == "__main__":
    main()

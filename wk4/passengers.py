import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('SQLALCHEMY_DATABASE_URI')
db = scoped_session(sessionmaker(bind=engine))

def main():

    # list all flights
    flights = db.execute("SELECT id, origin, destination, duration FROM flights")
    for flight in flights:
        print(f'Flight {flight.id}: {flight.origin} to {flight.destination}')

    # prompt user to choose a flight
    flight_id = int(input("\nFlight ID: "))
    flight = db.execute("SELECT origin, destination, duration FROM flights WHERE id = :id",
                        {"id": flight_id}).fetchall()

    # make sure flight is valid
    if flight is None:
        print('No such flight. Make sure flight number is correct.')
        return

    # list passengers
    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()

    print("\nPassengers:")
    for passenger in passengers:
        print(passenger.name)
    if len(passengers) == 0:
        print('No passengers.')

if __name__ == "__main__":
    main()

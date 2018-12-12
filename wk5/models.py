from flask_sqlalchemy import SQLAlchemy

# TODO: delete the 'please_delete' table from the week5 database

db = SQLAlchemy()

# one class = one table (from database)
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    passengers = db.relationship('Passenger', backref='flight', lazy=True)

    def add_passenger(self, name):
        p = Passenger(name=name, flight_id=self.id)
        db.session.add(p)
        db.session.commit()


class Passenger(db.Model):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)

class Testing(db.Model):
    __tablename__ = 'please_delete'
    id = db.Column(db.Integer, primary_key=True)
    col_1 = db.Column(db.String, nullable=False)
    col_2 = db.Column(db.Integer, nullable=False)

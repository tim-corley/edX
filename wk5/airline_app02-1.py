import os
from flask import Flask, render_template, jsonify, request
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_2')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    flights = Flight.query.all()
    return render_template('index.html', flights=flights)

@app.route('/book', methods=['POST'])
def book():
    # Get form information
    name = request.form.get('name')
    try:
        flight_id = int(request.form.get('flight_id'))
    except ValueError:
        return render_template('error.html', message='Invalid flight number.')

    # Make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template('error.html', message='No such flight with that id exists.')

    # Add passenger
    flight.add_passenger(name)
    return render_template('success.html')

@app.route('/flights')
def flights():
    flights = Flight.query.all()
    return render_template('flights.html', flights=flights)

@app.route('/flights/<int:flight_id>')
def flight(flight_id):
    # Make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template('error.html', message='No such flight exists.')

    # Get all Passengers
    # passengers = Passenger.query.filter_by(flight_id=flight_id).all()
    # can now do below b/c of passenger relationship config in models (ln14)
    passengers = flight.passengers
    return render_template('flight.html', flight=flight, passengers=passengers)

# create an endpoint
@app.route('/api/flights/<int:flight_id>')
def flight_api(flight_id):
    # Make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({'error': 'Invalid flight_id'}), 422

    # Get all passengers
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
        'origin': flight.origin,
        'destination': flight.destination,
        'duration': flight.duration,
        'passenger': names
    })

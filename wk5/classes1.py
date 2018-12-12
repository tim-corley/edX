class Flight:

    def __init__(self, origin, destination, duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration

def main():

    # create a Flight
    f = Flight(origin='New York', destination='Paris', duration=435)

    # change the value of a variable
    f.duration += 30

    # print details about the flight
    print(f.origin)
    print(f.destination)
    print(f.duration)

if __name__ == "__main__":
    main()    

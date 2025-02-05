from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime

#TODO: Reasearch clean CRUD operations for backend automation.
#TODO: How to interact with ingestion of data?
#      - For managing DB, can explore:
#         - Flask-Admin (need to Authenticate and Secure) - https://youtu.be/G1FBSYJ45Ww?si=eUmWc1oa62Sedyzi
#         - Webhook (endpoints that listen for POST requests) (need to Authenticate and Secure)
#         - API (endpoints that listen for GET/POST requests) (need to Authenticate and Secure)
#         
#      - Ask for CSV data and learn details of current ingestion to Google Sheets API

#TODO: Build UI Design, loading animation
#TODO: Build out baseline Front End View with current Model Setup

#example webhook
# @app.route('/webhook', methods=['POST'])
# def handle_webhook():
#     data = request.json  # Get JSON payload from webhook
#     print("Received webhook data:", data)
#     # Process the data here (e.g., update database, trigger actions)
#     return jsonify({"message": "Webhook received!"}), 200

def fetch_or_create_driver(driver_name):
    driver = db.session.query(Driver).filter_by(driver_name=driver_name).first()
    if driver is None:
        driver = Driver(driver_name=driver_name)
        db.session.add(driver)
        db.session.commit()
        print(f"Driver {driver_name} created.")
    return driver

def fetch_or_create_event(event_name):
    event = db.session.query(Event).filter_by(event_name=event_name).first()
    if event is None:
        event = Event(event_name=event_name)
        db.session.add(event)
        db.session.commit()
        print(f"Event {event_name} created.")
    return event

def fetch_or_create_car(car_name, car_class):
    car = db.session.query(Car).filter_by(car_name=car_name, car_class=car_class).first()
    if car is None:
        car = Car(car_name=car_name, car_class=car_class)
        db.session.add(car)
        db.session.commit()
        print(f"Car {car_name} ({car_class}) created.")
    return car

def create_driverEvent(driver_name, event_name, car_name, car_class):

    # Assuming you have already imported the necessary modules and set up the session
    # Retrieve the existing driver, event, car, and car_class instances
    driver = db.session.query(Driver).filter_by(driver_name=driver_name).first()
    event = db.session.query(Event).filter_by(event_name=event_name).first()
    car = db.session.query(Car).filter_by(car_name=car_name, car_class=car_class).first()

    if driver is None:
        add_driver(driver_name)
        driver = db.session.query(Driver).filter_by(driver_name=driver_name).first()

    if event is None:
        add_event(event_name)
        event = db.session.query(Event).filter_by(event_name=event_name).first()

    if car is None:
        add_car(car_name, car_class)
        car = db.session.query(Car).filter_by(car_name=car_name, car_class=car_class).first()

    # Ensure the instances exist
    if driver and event and car:
        try:
            # Create the DriverEvent instance
            driver_event = DriverEvent(driver=driver, event=event, car=car)
            db.session.add(driver_event)
            db.session.commit()
            print("DriverEvent created successfully.")

        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError occurred: {e}")
    else:
        print("One or more instances not found.")
        print(f"Driver: {driver}, Event: {event}, Car: {car}")

def update_or_create_driverEventStats(my_laptime):
    print("-"*20)
    print(f"Running Event Listener for {my_laptime}")
    print(f"Driver Event: {my_laptime.driver_event}")

    laptimes = db.session.query(Laptime).filter_by(driver_event=my_laptime.driver_event).all()
    this_laps_driverEventStats = db.session.query(DriverEventStats).filter_by(driver_event=my_laptime.driver_event).first()
    total_runs = len(laptimes)
    total_time = sum((lt.laptime for lt in laptimes), timedelta())
    avg_laptime = total_time / total_runs 
    min_laptime = min((lt.laptime for lt in laptimes), default=None)
    max_laptime = max((lt.laptime for lt in laptimes), default=None)

    print(f"Total Runs: {total_runs}")
    print(f"Total Time: {total_time}")
    print(f"Average Laptime: {avg_laptime}")


    if this_laps_driverEventStats is None:
        print(f"Creating new DriverEventStats for {my_laptime.driver_event} -------")

        set_driver_event_stats = DriverEventStats(
            driver_event_id=my_laptime.driver_event.id,
            fastest_lap=min_laptime,
            average_lap=avg_laptime,
            total_laps=total_runs
            )
        
        db.session.add(set_driver_event_stats)

    if this_laps_driverEventStats:

        print(f"Updating existing DriverEventStats for {this_laps_driverEventStats} -------")
        print(f"total laps before update: {this_laps_driverEventStats.total_laps}")


        this_laps_driverEventStats.total_laps = total_runs
        this_laps_driverEventStats.fastest_lap = min_laptime
        this_laps_driverEventStats.average_lap = avg_laptime
        

        print(f"total laps after update: {this_laps_driverEventStats.total_laps}")


    


# @event.listens_for(Laptime, 'after_insert')
# def after_insert_laptime(mapper, connection, target):
#     print(f"Running Event Listener AFTER INSERT for {target}")
#     add_driver_event_stats(target)

# @event.listens_for(Laptime, 'after_update')
# def after_update_laptime(mapper, connection, target):
#     print(f"Running Event Listener AFTER UPDATE for {target}")
#     update_driver_event_stats(target)

# @event.listens_for(Laptime, 'after_delete')
# def after_delete_laptime(mapper, connection, target):
#     print(f"Running Event Listener AFTER DELETE for {target}")
#     update_driver_event_stats(target)

# @event.listens_for(db.session, 'after_flush')
# def after_flush(session, context):
#     print(f"New instances in session: {session.new}")
#     for instance in session.new:
#         if isinstance(instance, Laptime):
#             print(f"Running Event Listener AFTER FLUSH for {instance}")
#             update_driver_event_stats(instance)





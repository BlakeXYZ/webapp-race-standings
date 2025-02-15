from datetime import date, timezone, timedelta
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime

#TODO: Reasearch clean CRUD operations for backend automation.
#TODO: How to interact with ingestion of data?
#      - For managing DB, can explore:
#         - Flask-Admin (need to Authenticate and Secure) - https://youtu.be/G1FBSYJ45Ww?si=eUmWc1oa62Sedyzi
#         - Webhook (endpoints that listen for POST requests) (need to Authenticate and Secure)
#                Use webhooks if an external service needs to push data to your app automatically.
#                Use API endpoints if your app needs to fetch or update data on demand.
#                Combine both for efficient real-time data processing.   
#
# When to Use a Webhook?
#
# ✅ When an external service needs to notify your app in real time.
#
#     A Google Sheet cell is updated → Sends webhook to your Flask app.
#     A new payment is made in Stripe → Sends webhook to update your database.
#     A GitHub commit is pushed → Sends webhook to trigger a CI/CD build.
#
# 🔹 Best for: Receiving event-based updates automatically.
# 🔹 Downside: If your server is down, you may miss the update unless retries are built in.


# When to Use an API Endpoint?
#
# ✅ When your app needs to request or modify data on demand.
#
#     Your frontend calls /users/1 to get a user’s profile.
#     A script calls /products to fetch a product list.
#     A mobile app submits a form via /submit-form.
#
# 🔹 Best for: On-demand interactions where you need full control.
# 🔹 Downside: If polling frequently, can waste resources and cause delays.

# 
# 
#  
#TODO:  - Ask for CSV data and learn details of current ingestion to Google Sheets API


#TODO: Build UI Design, loading animation
#TODO: Build out baseline Front End View with current Model Setup. **Show Proof of Concept!**

#example webhook
# @app.route('/webhook', methods=['POST'])
# def handle_webhook():
#     data = request.json  # Get JSON payload from webhook
#     print("Received webhook data:", data)
#     # Process the data here (e.g., update database, trigger actions)
#     return jsonify({"message": "Webhook received!"}), 200


#TODO: DB management. Do we want to auto Create if Fetch fails? What is CRUD Best practices?

def add_item(db_session, model, **kwargs):
    if not kwargs:
        raise ValueError(f"{model.__name__} attributes cannot be None or empty")
    if not all(hasattr(model, attr) for attr in kwargs.keys()):
        raise ValueError(f"{model.__name__} does not have all the required attributes")
    for attr, value in kwargs.items():
        column = getattr(model, attr)
        if hasattr(column, 'property') and hasattr(column.property, 'columns'):
            column_type = column.property.columns[0].type.python_type
            if not isinstance(value, column_type):
                raise ValueError(f"Value for {attr} must be of type {column_type}")
        elif hasattr(column, 'mapper'):
            if not isinstance(value, column.mapper.class_):
                raise ValueError(f"Value for {attr} must be of type {column.mapper.class_}")
        else:
            raise ValueError(f"Value for {attr} must be of type {type(column)}")

    item = model(**kwargs)
    db_session.add(item)
    return item

def add_driver(db_session, driver_name):
    return add_item(db_session, Driver, driver_name=driver_name)

def add_event(db_session, event_name, event_date):
    return add_item(db_session, Event, event_name=event_name, event_date=event_date)

def add_car(db_session, car_name, car_class):
    return add_item(db_session, Car, car_name=car_name, car_class=car_class)
    
def add_driverEvent(db_session, driver_name, event_name, event_date, car_name, car_class):
    driver = db_session.query(Driver).filter_by(driver_name=driver_name).first()
    event = db_session.query(Event).filter_by(event_name=event_name, event_date=event_date).first()
    car = db_session.query(Car).filter_by(car_name=car_name, car_class=car_class).first()

    if driver is None:
        driver = add_driver(db_session, driver_name)

    if event is None:
        event = add_event(db_session, event_name, event_date)

    if car is None:
        car = add_car(db_session, car_name, car_class)
    
    if driver and event and car:
        return add_item(db_session, DriverEvent, driver=driver, event=event, car=car)
    else:
        return None






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

# #TODO how best to query info for laptime add?
def add_laptime(db_session, driver_event_id, laptime):
    driver_event = db_session.query(DriverEvent).filter_by(id=driver_event_id).first()
    if driver_event is None:
        raise ValueError(f"DriverEvent with id {driver_event_id} does not exist")

    #dynamicallly get run_number
    laptimes = db_session.query(Laptime).filter_by(driver_event=driver_event).all()

    print(f"laptime count: {len(laptimes)}") 

    return add_item(db_session, Laptime, driver_event_id=driver_event_id, laptime=laptime, run_number=len(laptimes)+1)
    







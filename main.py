import subprocess
from datetime import date, datetime, timezone, timedelta

import sqlalchemy as sa
import sqlalchemy.orm as so 

from app import app, db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime


@app.shell_context_processor
def make_shell_context():
    return {
        'date': date,
        'timedelta': timedelta,
        'sa': sa, 
        'so': so, 
        'db': db, 
        'Driver': Driver, 
        'Event': Event,
        'Car': Car,
        'Laptime': Laptime,
        'gad': get_all_drivers,
        'gae': get_all_events,
        'gac': get_all_cars,
        'gde': get_driver_events,
        'gdes': get_driver_event_stats,
        'gl': get_laptimes,
        'trunc': truncate_tables,
        'udes': update_driver_event_stats,
        'ad': add_driver,
        'ae': add_event,
        'ac': add_car,
        'ade': add_driverEvent,

    }

def get_all_drivers():
    """Utility function to get all users from the database."""
    query = sa.select(Driver)
    drivers = db.session.scalars(query)
    print('Printing all drivers:')
    for u in drivers:
        print(f'id: {u.id} driver_name: {u.driver_name}')

def get_all_events():
    """Utility function to get all events from the database."""
    query = sa.select(Event)
    events = db.session.scalars(query)
    print('Printing all events:')
    for u in events:
        print(f'id: {u.id} event_name: {u.event_name} event_date: {u.event_date}')

def get_all_cars():
    """Utility function to get all cars from the database."""
    query = sa.select(Car)
    cars = db.session.scalars(query)
    print('Printing all cars:')
    for u in cars:
        print(f'id: {u.id} car_name: {u.car_name} car_class: {u.car_class}')

def get_driver_events():
    """Utility function to get all driver events from the database."""
    query = sa.select(DriverEvent)
    driver_events = db.session.scalars(query)
    print('Printing all driver events:')
    for u in driver_events:
        print(f'id: {u.id} driver_name: {u.driver.driver_name} event_name: {u.event.event_name} car_name: {u.car.car_name} car_class: {u.car.car_class}')

def get_driver_event_stats():
    """Utility function to get all driver event stats from the database."""
    query = sa.select(DriverEventStats)
    driver_event_stats = db.session.scalars(query)
    print('Printing all driver event stats:')
    for u in driver_event_stats:
        print(f'id: {u.id} driver_event_id: {u.driver_event_id} avg_laptime: {u.avg_laptime}')

def get_laptimes():
    """Utility function to get all laptimes from the database."""
    query = sa.select(Laptime)
    laptimes = db.session.scalars(query)
    print('Printing all laptimes:')
    for u in laptimes:
        print(f'id: {u.id} driver_event_id: {u.driver_event_id} run_number: {u.run_number}')

def truncate_tables():
    """Utility function to truncate all tables in the database."""
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Truncating table {table}')
        db.session.execute(table.delete())
    db.session.commit()

def running_flask_app():
    # Command to run Flask
    command = ['flask', '--app', 'main', 'run', '--reload']

    # Use subprocess to run the command
    process = subprocess.Popen(command, shell=True)

    # Optionally, wait for the process to complete
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()

if __name__ == '__main__':

    running_flask_app()
    
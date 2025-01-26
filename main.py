import subprocess
from datetime import date, timedelta
import sqlalchemy as sa
import sqlalchemy.orm as so 

from app import app, db
from app.models import Driver, Event, Laptime


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
        'Laptime': Laptime,
        'gad': get_all_drivers,
        'gae': get_all_events,
        'trunc': truncate_tables
    }

def get_all_drivers():
    """Utility function to get all users from the database."""
    query = sa.select(Driver)
    drivers = db.session.scalars(query)
    print('Printing all drivers:')
    for u in drivers:
        print(f'id: {u.id} driver_name: {u.driver_name} driver_car: {u.driver_car}')

def get_all_events():
    """Utility function to get all events from the database."""
    query = sa.select(Event)
    events = db.session.scalars(query)
    print('Printing all events:')
    for u in events:
        print(f'id: {u.id} event_name: {u.event_name} event_date: {u.event_date}')

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
    
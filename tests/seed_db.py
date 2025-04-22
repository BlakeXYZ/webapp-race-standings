import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # So we can import app

import datetime
import random
import sqlalchemy as sa
import sqlalchemy.orm as so 

from app import app, db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime
from app.db_commit_helpers import add_season, add_event_type, add_laptime
from config import Config

from factories import EventFactory, DriverFactory, CarFactory, DriverEventFactory

def seed_db():
    with app.app_context():  # Set up the application context
        db.drop_all()
        db.create_all()


        add_season(db.session, season_name='2023', start_date=datetime.date(2023, 1, 1), end_date=datetime.date(2023, 12, 31))
        add_season(db.session, season_name='2024', start_date=datetime.date(2024, 1, 1), end_date=datetime.date(2024, 12, 31))
        add_season(db.session, season_name='2025', start_date=datetime.date(2025, 1, 1), end_date=datetime.date(2025, 12, 31))
        add_event_type(db.session, event_type_name='Points')
        add_event_type(db.session, event_type_name='Practice')

        # Create a batch of 2 events
        events = EventFactory.create_batch(2)
        # Create a batch of 2 drivers
        drivers = DriverFactory.create_batch(5)

        # Create a batch of 5 DriverEvent instances and assign events randomly
        driver_events = [
            DriverEventFactory(driver=driver, event=event)
            for driver in drivers
            for event in events
        ]

        _generate_laptimes(laptime_count=8)



        db.session.commit()
        print("Database seeded successfully!")


def _generate_laptimes(laptime_count: int):
    """Generate random laptimes for testing."""

    driverEvent_count = db.session.query(DriverEvent).count()
    print(f"Generating {laptime_count} laptimes for {driverEvent_count} driver events.")

    for driver_event in range(driverEvent_count):
        for _ in range(random.randint(laptime_count - 2, laptime_count)):
            add_laptime(
                db.session,
                driver_event_id=driver_event + 1,
                laptime=round(random.uniform(60, 120), 2),  # Random laptime between 60 and 120 seconds with 2 decimal places
            )


if __name__ == "__main__":
    seed_db()

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # So we can import app

import datetime
import factory
from faker import Faker
from app.models import Driver, Event, Car, DriverEvent
from app import db

fake = Faker()

class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = db.session

    event_name = factory.Sequence(lambda n: f"Event-{n}-{fake.word()}")
    event_date = factory.LazyFunction(lambda: fake.date_between(start_date=datetime.date(2025, 1, 1), end_date=datetime.date(2025, 12, 31)))
    event_type_id = 1  # Assuming you have an EventType with id=1 in your database

class DriverFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Driver
        sqlalchemy_session = db.session

    driver_name = factory.Sequence(lambda n: f"Driver-{n}-{fake.name()}")

class CarFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Car
        sqlalchemy_session = db.session

    car_name = factory.Sequence(lambda n: f"Car-{n}-{fake.word()}")
    car_class = factory.LazyFunction(lambda: fake.random_element(elements=["RWD", "AWD"]))


class DriverEventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DriverEvent
        sqlalchemy_session = db.session

    driver = factory.SubFactory(DriverFactory)  # Generates a related Driver instance
    event = factory.SubFactory(EventFactory)    # Generates a related Event instance
    car = factory.SubFactory(CarFactory)        # Generates a related Car instance


    
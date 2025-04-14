import datetime
import unittest
import sqlalchemy as sa
import sqlalchemy.orm as so 
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime
from app.db_commit_helpers import add_driverEvent, add_laptime, add_event
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'



class DriverEventModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_driver(self):
    #     d = Driver(driver_name='test_driver')
    #     db.session.add(d)
    #     db.session.commit()
    #     self.assertEqual(d.driver_name, 'test_driver')

    # def test_lap(self):
    #     print(f"UNITTEST - Running test_lap ------------------------ ")
    #     d = Driver(driver_name='Joe Bobby')
    #     e = Event(event_name='Grand Prix', event_date=datetime.now(timezone.utc))
    #     c = Car(car_name='Mercedes', car_class='S Class')
    #     de = DriverEvent(driver=d, event=e, car=c)
    #     db.session.add_all([d, e, c, de])
    #     db.session.commit()

    #     """Utility function to get all cars from the database."""
    #     query = sa.select(Car)
    #     cars = db.session.scalars(query)
    #     print('Printing all cars:')
    #     for u in cars:
    #         print(f'id: {u.id} car_name: {u.car_name} car_class: {u.car_class}')


    #     """Utility function to get all driver events from the database."""
    #     query = sa.select(DriverEvent)
    #     driver_events = db.session.scalars(query)
    #     print('Printing all driver events:')
    #     for u in driver_events:
    #         print(f'id: {u.id} driver_id: {u.driver_id} event_id: {u.event_id} event_name: {u.event.event_name} -- driver name: {u.driver.driver_name}')


    #     event = db.session.query(Event).filter_by(event_name='Grand Prix').first()
    #     d = Driver(driver_name='Jack')
    #     c = Car(car_name='Subaru', car_class='AWD')
    #     de = DriverEvent(driver=d, event=event, car=c)
    #     db.session.add_all([d, c, de])
    #     db.session.commit()

    #     # #query all driver events
    #     driver_events = db.session.query(DriverEvent).all()
    #     print(f"Printing all driver events: {driver_events}")


    #     # l = Laptime(driver_event=de, laptime=timedelta(minutes=1, seconds=30), run_number=1)
    #     # db.session.add(l)               ###########
    #     # update_driver_event_stats(l)    ###########
    #     # db.session.commit()             ###########
    #     # print(f"session committed")
    #     # stats = db.session.query(DriverEventStats).filter_by(driver_event=de).first() 
    #     # print(f"Stats: {stats}")

    #     # #query all laps
    #     # laptimes = db.session.query(Laptime).filter_by(driver_event=de).all()
    #     # print(f"Printing all laptimes: {laptimes}")          

    #     # print(f"ADDING SECOND LAP -------------------------------------------------------")
    #     # l_2 = Laptime(driver_event=de, laptime=timedelta(minutes=3, seconds=30), run_number=2)
    #     # db.session.add(l_2)             ###########
    #     # update_driver_event_stats(l_2)  ###########   
    #     # db.session.commit()             ###########
    #     # print(f"session committed")
    #     # stats = db.session.query(DriverEventStats).filter_by(driver_event=de).first()
    #     # print(f"New Stats after adding 2nd lap: {stats}")


    #     # #query all laps
    #     # laptimes = db.session.query(Laptime).filter_by(driver_event=de).all()
    #     # print(f"Printing all laptimes: {laptimes}")


    def test_add_driver(self):
        print(f"UNITTEST - Running test_add_driver ------------------------ ")
        driver_name = 'Joe Bobby'
        d = add_driver(db.session, driver_name)

        try:
            db.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

        except IntegrityError as e:
            print(f"Error: {e}")
            db.session.rollback()


    def test_add_driverEvent(self):
        print(f"UNITTEST - Running test_create_driverEvent ------------------------ ")
        driver_name = 'Joe Bobby'
        event_name = 'Grand Prix'
        event_date = datetime.date(2024, 1, 1)
    
        car_name = 'Mercedes'
        car_class = 'S Class'

        de = add_driverEvent(db.session, driver_name, event_name, event_date, car_name, car_class)

        a = add_laptime(db.session, driver_event_id=1, laptime=datetime.timedelta(seconds=145))
        print(f"Laptime: {a}")
        print(f"DriverEvent: {de}")

        a = add_laptime(db.session, driver_event_id=1, laptime=datetime.timedelta(minutes=2, seconds=10))
        print(f"Laptime: {a}")
        print(f"DriverEvent: {de}")

        a = add_laptime(db.session, driver_event_id=1, laptime=datetime.timedelta(minutes=3, seconds=00))
        print(f"Laptime: {a}")
        print(f"DriverEvent: {de}")


        try:
            db.session.commit()

        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

        except IntegrityError as e:
            print(f"Error: {e}")
            db.session.rollback()

    def test_add_event(self):
        print(f"UNITTEST - Running test_add_event ------------------------ ")
        event_name = 'Grand Prix'
        event_date = datetime.date(2024, 1, 1)
        event_type_name = 'Practice Event'
        season_name = '2024 Season'
        add_event(db.session, event_name, event_date, season_name, event_type_name)

        try:
            db.session.commit()
            events = db.session.query(Event).all()
            print(f"Printing all events: {events}")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

        except IntegrityError as e:
            print(f"Error: {e}")
            db.session.rollback()


if __name__ == '__main__':
    # unittest.main(verbosity=2)

    suite = unittest.TestSuite()
    suite.addTest(DriverEventModelCase('test_add_event'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
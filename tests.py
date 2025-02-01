from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime
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

    def test_driver(self):
        d = Driver(driver_name='test_driver')
        db.session.add(d)
        db.session.commit()
        self.assertEqual(d.driver_name, 'test_driver')

    def test_lap(self):
        d = Driver(driver_name='Joe Bobby')
        e = Event(event_name='Grand Prix', event_date=datetime.now(timezone.utc))
        c = Car(car_name='Mercedes', car_class='S Class')
        de = DriverEvent(driver=d, event=e, car=c)
        db.session.add_all([d, e, c, de])
        db.session.commit()
        

        l = Laptime(driver_event=de, laptime=timedelta(minutes=1, seconds=30), run_number=1)
        db.session.add(l)
        db.session.commit()
        stats = db.session.query(DriverEventStats).filter_by(driver_event=de).first()
        print(f"Stats: {stats}")
            
                        

        l_2 = Laptime(driver_event=de, laptime=timedelta(minutes=1, seconds=40), run_number=2)
        db.session.add(l_2)
        db.session.commit()


if __name__ == '__main__':
    # unittest.main(verbosity=2)

    suite = unittest.TestSuite()
    suite.addTest(DriverEventModelCase('test_lap'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
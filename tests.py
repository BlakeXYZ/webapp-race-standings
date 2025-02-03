from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

def update_driver_event_stats(target):
    print("-"*20)
    print(f"Running Event Listener for {target}")
    print(f"Driver Event: {target.driver_event}")

    laptimes = db.session.query(Laptime).filter_by(driver_event=target.driver_event).all()
    this_laps_driverEventStats = db.session.query(DriverEventStats).filter_by(driver_event=target.driver_event).first()
    total_runs = len(laptimes)
    total_time = sum((lt.laptime for lt in laptimes), timedelta())
    avg_laptime = total_time / total_runs 
    min_laptime = min((lt.laptime for lt in laptimes), default=None)
    max_laptime = max((lt.laptime for lt in laptimes), default=None)

    print(f"Total Runs: {total_runs}")
    print(f"Total Time: {total_time}")
    print(f"Average Laptime: {avg_laptime}")


    if this_laps_driverEventStats is None:
        print(f"Creating new DriverEventStats for {target.driver_event} -------")

        set_driver_event_stats = DriverEventStats(
            driver_event_id=target.driver_event.id,
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




# def hello_world():
#     print("Hello World")

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
        print(f"UNITTEST - Running test_lap ------------------------ ")
        d = Driver(driver_name='Joe Bobby')
        e = Event(event_name='Grand Prix', event_date=datetime.now(timezone.utc))
        c = Car(car_name='Mercedes', car_class='S Class')
        de = DriverEvent(driver=d, event=e, car=c)
        db.session.add_all([d, e, c, de])
        db.session.commit()

        l = Laptime(driver_event=de, laptime=timedelta(minutes=1, seconds=30), run_number=1)
        db.session.add(l)               ###########
        update_driver_event_stats(l)    ###########
        db.session.commit()             ###########
        print(f"session committed")
        stats = db.session.query(DriverEventStats).filter_by(driver_event=de).first()
        print(f"Stats: {stats}")

        #query all laps
        laptimes = db.session.query(Laptime).filter_by(driver_event=de).all()
        print(f"Printing all laptimes: {laptimes}")          

        print(f"ADDING SECOND LAP -------------------------------------------------------")
        l_2 = Laptime(driver_event=de, laptime=timedelta(minutes=3, seconds=30), run_number=2)
        db.session.add(l_2)             ###########
        update_driver_event_stats(l_2)  ###########   
        db.session.commit()             ###########
        print(f"session committed")
        stats = db.session.query(DriverEventStats).filter_by(driver_event=de).first()
        print(f"New Stats after adding 2nd lap: {stats}")


        #query all laps
        laptimes = db.session.query(Laptime).filter_by(driver_event=de).all()
        print(f"Printing all laptimes: {laptimes}")

if __name__ == '__main__':
    # unittest.main(verbosity=2)

    suite = unittest.TestSuite()
    suite.addTest(DriverEventModelCase('test_lap'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
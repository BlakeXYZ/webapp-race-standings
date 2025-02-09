from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Driver, Event, Car, DriverEvent, DriverEventStats, Laptime


def update_driver_event_stats(my_laptime):
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





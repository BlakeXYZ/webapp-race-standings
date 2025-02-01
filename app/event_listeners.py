from sqlalchemy import event
import datetime

from app import db
from app.models import Laptime, DriverEvent, DriverEventStats

# def update_driver_event_stats(driver_id, event_id):
#     print(f"Updating stats for driver {driver_id} at event {event_id}")
#     laptimes = db.session.query(Laptime).filter_by(driver_id=driver_id, event_id=event_id).all()
#     total_runs = len(laptimes)
#     total_time = sum((lt.laptime for lt in laptimes), datetime.timedelta())
#     avg_laptime = total_time / total_runs if total_runs > 0 else None
#     min_laptime = min((lt.laptime for lt in laptimes), default=None)
#     max_laptime = max((lt.laptime for lt in laptimes), default=None)

#     driver_event = db.session.query(DriverEvent).filter_by(driver_id=driver_id, event_id=event_id).first()
#     if driver_event:
#         if not driver_event.stats:
#             driver_event.stats = DriverEventStats(driver_event=driver_event.id)
#         driver_event.stats.avg_laptime = avg_laptime
#         driver_event.stats.total_runs = total_runs
#         driver_event.stats.min_laptime = min_laptime
#         driver_event.stats.max_laptime = max_laptime
#         driver_event.stats.total_time = total_time
#         db.session.commit()

def update_driver_event_stats(target):
    print("-"*20)
    print(f"Running Event Listener for {target}")
    print(f"Driver Event: {target.driver_event}")

    laptimes = db.session.query(Laptime).filter_by(driver_event=target.driver_event).all()
    total_runs = len(laptimes)
    total_time = sum((lt.laptime for lt in laptimes), datetime.timedelta())
    avg_laptime = total_time / total_runs if total_runs > 0 else None
    min_laptime = min((lt.laptime for lt in laptimes), default=None)
    max_laptime = max((lt.laptime for lt in laptimes), default=None)

    print(f"Total Runs: {total_runs}")



    if not target.driver_event.driver_event_stats:
        print(f"Creating new DriverEventStats for {target.driver_event}")

        set_driver_event_stats = DriverEventStats(
            driver_event_id=target.driver_event.id,
            fastest_lap=min_laptime,
            average_lap=avg_laptime,
            total_laps=total_runs
            )

    # set_driver_event_stats.fastest_lap = min_laptime
    # set_driver_event_stats.average_lap = avg_laptime
    # set_driver_event_stats.total_laps = total_runs
    db.session.add(set_driver_event_stats)

    print("="*80)
    print("="*80)


# @event.listens_for(Laptime, 'after_insert')
# def after_insert_laptime(mapper, connection, target):
#     print(f"Running Event Listener AFTER INSERT for {target}")
#     update_driver_event_stats(target)

# @event.listens_for(Laptime, 'after_update')
# def after_update_laptime(mapper, connection, target):
#     print(f"Running Event Listener AFTER UPDATE for {target}")
#     update_driver_event_stats(target)

# @event.listens_for(Laptime, 'after_delete')
# def after_delete_laptime(mapper, connection, target):
#     print(f"Running Event Listener AFTER DELETE for {target}")
#     update_driver_event_stats(target)

@event.listens_for(db.session, 'after_flush')
def after_flush(session, context):
    for instance in session.new:
        if isinstance(instance, Laptime):
            print(f"Running Event Listener AFTER FLUSH for {instance}")
            update_driver_event_stats(instance)





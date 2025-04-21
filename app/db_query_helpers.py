from sqlalchemy import desc
from app import db
from app.models import Season, EventType, Driver, Event, Car, DriverEvent, DriverEventStats, Laptime

# Query to find the DriverEventStats with the most laps for a specific event
def get_driver_event_stats_with_most_laps(event_id):
    query = (
        db.session.query(DriverEventStats)
        .join(DriverEvent, DriverEventStats.driver_event_id == DriverEvent.id)
        .filter(DriverEvent.event_id == event_id)
        .order_by(desc(DriverEventStats.total_laps))
        .first()
    )
    
    return query.total_laps if query else None
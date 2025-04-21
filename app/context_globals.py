
from app.models import Driver, Event
from app import app, db
import sqlalchemy as sa

@app.context_processor
def inject_globals():
    drivers = db.session.scalars(sa.select(Driver)).all()
    events = db.session.scalars(sa.select(Event)).all()

    return {
        'drivers': drivers,
        'events': events
    }
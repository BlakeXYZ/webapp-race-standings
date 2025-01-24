from typing import Optional
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

    
class Driver(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    driver_car: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Driver {}>'.format(self.driver_name)

class Event(db.Model):
    """
    example event add to db:

    new_event = Event(event_name='Grand Prix', event_date=date(2024, 4, 1))
    db.session.add(new_event)
    db.session.commit()
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    event_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    event_date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)

    def __repr__(self):
        return '<Event {}>'.format(self.event_name)
    


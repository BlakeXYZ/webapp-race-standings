from typing import Optional
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

#TODO: How to account for driver having a unique car for each event?
class Driver(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    driver_car: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    laptimes: so.Mapped[list["Laptime"]] = so.relationship("Laptime", back_populates="driver")

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

    laptimes: so.Mapped[list["Laptime"]] = so.relationship("Laptime", back_populates="event")

    def __repr__(self):
        return '<Event {}>'.format(self.event_name)
    
class Laptime(db.Model):
    """
    example laptime add to db:

    new_laptime = Laptime(driver_id=1, event_id=1, laptime=timedelta(minutes=1, seconds=30))

    db.session.add(new_laptime)
    db.session.commit()
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('driver.id'))
    event_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('event.id'))
    laptime: so.Mapped[datetime.timedelta] = so.mapped_column(sa.Interval)

    driver: so.Mapped["Driver"] = so.relationship("Driver", back_populates="laptimes")
    event: so.Mapped["Event"] = so.relationship("Event", back_populates="laptimes")

    def __repr__(self):
        return '<Laptime {}>'.format(self.laptime)

    

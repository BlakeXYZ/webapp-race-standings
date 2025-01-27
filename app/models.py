from typing import Optional
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from slugify import slugify  
from app import db



#TODO: How to account for driver having a unique car for each event?
class Driver(db.Model):
    """
    example driver add to db:

    new_driver = Driver(driver_name='John Doe')
    db.session.add(new_event)
    db.session.commit()
    
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    driver_events: so.Mapped[list["DriverEvent"]] = so.relationship("DriverEvent", back_populates="driver")

    def __repr__(self):
        return '<Driver {}>'.format(self.driver_name)
    
    def get_slug(self):
        return slugify(self.driver_name)


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

    driver_events: so.Mapped[list["DriverEvent"]] = so.relationship("DriverEvent", back_populates="event")

    def __repr__(self):
        return '<Event {}>'.format(self.event_name)
    

class DriverEvent(db.Model):
    """
    Association table to link drivers to events with unique cars and classes.

    example driver_event add to db:

    new_driver_event = DriverEvent(driver_id=1, event_id=1, car='Subaru', car_class='AWD')
        
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('driver.id'))
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('event.id'))
    car: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    car_class: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    driver: so.Mapped["Driver"] = so.relationship("Driver", back_populates="driver_events")
    event: so.Mapped["Event"] = so.relationship("Event", back_populates="driver_events")
    laptimes: so.Mapped[list["Laptime"]] = so.relationship("Laptime", back_populates="driver_event")

    def __repr__(self):
        return '<DriverEvent driver={} event={} car={} car_class={}>'.format(
            self.driver.driver_name, self.event.event_name, self.car, self.car_class
        )

class Laptime(db.Model):
    """
    example laptime add to db:

    new_laptime = Laptime(driver_event_id=1, laptime=timedelta(minutes=1, seconds=30), run_number=1)

    db.session.add(new_laptime)
    db.session.commit()
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('driver_event.id'))
    laptime: so.Mapped[datetime.timedelta] = so.mapped_column(sa.Interval)
    run_number: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)

    driver_event: so.Mapped["DriverEvent"] = so.relationship("DriverEvent", back_populates="laptimes")

    def __repr__(self):
        return '<Laptime run={} time={}>'.format(self.run_number, self.laptime)
    

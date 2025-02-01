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
    db.session.add(new_driver)
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
    
class Car(db.Model):
    """
    example car add to db:

    new_car = Car(car_name='Subaru', car_class='AWD')
    db.session.add(new_car)
    db.session.commit()
    """

    __table_args__ = (sa.UniqueConstraint('car_name', 'car_class', name='unique_car'),)

    id:         so.Mapped[int] = so.mapped_column(primary_key=True)
    car_name:   so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    car_class:  so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    driver_events: so.Mapped[list["DriverEvent"]] = so.relationship("DriverEvent", back_populates="car")

    def __repr__(self):
        return '<Car {}>'.format(self.car_name)
    
class DriverEvent(db.Model):
    """
    Association table to link drivers to events with unique cars and classes.

    example driver_event add to db:

    new_driver_event = DriverEvent(driver_id=1, event_id=1, car='Subaru', car_class='AWD')
        
    """
    # prevents duplicate entries for the same driver, event, and car combination
    __table_args__ = (sa.UniqueConstraint('driver_id', 'event_id', 'car_id', name='unique_driver_event'),)

    id:         so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_id:  so.Mapped[int] = so.mapped_column(sa.ForeignKey('driver.id'), index=True)
    event_id:   so.Mapped[int] = so.mapped_column(sa.ForeignKey('event.id'), index=True)
    car_id:     so.Mapped[int] = so.mapped_column(sa.ForeignKey('car.id'), index=True)

    driver:     so.Mapped["Driver"] = so.relationship("Driver", back_populates="driver_events")
    event:      so.Mapped["Event"] = so.relationship("Event", back_populates="driver_events")
    car:        so.Mapped["Car"] = so.relationship("Car", back_populates="driver_events")

    laptimes:           so.Mapped[list["Laptime"]] = so.relationship("Laptime", back_populates="driver_event")
    driver_event_stats: so.Mapped[list["DriverEventStats"]] = so.relationship("DriverEventStats", back_populates="driver_event")

    def __repr__(self):
        return f"<DriverEvent driver={self.driver.driver_name} event={self.event.event_name} car={self.car.car_name} ({self.car.car_class})>"
        
#TODO: store more statistics that are calculated from Laptimes (do it on the fly or store them in a separate table?)
# this setup may be improper workflow?
class DriverEventStats(db.Model):
    """
    example driver_event_stats add to db:

    new_driver_event_stats = DriverEventStats(driver_event_id=1, fastest_lap=timedelta(minutes=1, seconds=30), total_laps=10)

    db.session.add(new_driver_event_stats)
    db.session.commit()
    """
    id:                 so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_event_id:    so.Mapped[int] = so.mapped_column(sa.ForeignKey('driver_event.id'), unique=True, index=True)

    fastest_lap:        so.Mapped[Optional[datetime.timedelta]] = so.mapped_column(sa.Interval)
    average_lap:        so.Mapped[Optional[datetime.timedelta]] = so.mapped_column(sa.Interval)
    total_laps:         so.Mapped[int] = so.mapped_column(sa.Integer, index=True)

    driver_event: so.Mapped["DriverEvent"] = so.relationship("DriverEvent", back_populates="driver_event_stats")

    def __repr__(self):
        return '<DriverEventStats driver_event={} fastest_lap={} total_laps={}>'.format(
            self.driver_event, self.fastest_lap, self.total_laps
        )

class Laptime(db.Model):
    """
    example laptime add to db:

    new_laptime = Laptime(driver_event_id=1, laptime=timedelta(minutes=1, seconds=30), run_number=1)

    db.session.add(new_laptime)
    db.session.commit()
    """
    id:                 so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_event_id:    so.Mapped[int] = so.mapped_column(sa.ForeignKey('driver_event.id'))
    
    laptime:            so.Mapped[datetime.timedelta] = so.mapped_column(sa.Interval)
    run_number:         so.Mapped[int] = so.mapped_column(sa.Integer, index=True)

    driver_event:       so.Mapped["DriverEvent"] = so.relationship("DriverEvent", back_populates="laptimes")

    def __repr__(self):
        return '<Laptime run={} time={}>'.format(self.run_number, self.laptime)
    

from asyncio import events
from typing import Optional
import datetime 
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import validates
from slugify import slugify  
from app import db

#TODO find alternative to datetime? outdated? datetime2 perhaps?


class Season(db.Model):
    """
    example season add to db:

    new_season = Season(season_name='2024, start_date=date(2024, 4, 1), end_date=date(2024, 12, 31))
    db.session.add(new_season)
    """
    id:             so.Mapped[int] = so.mapped_column(primary_key=True)
    season_name:    so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    start_date:     so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
    end_date:       so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)

    events: so.Mapped[list["Event"]] = so.relationship("Event", back_populates="season")

    def __repr__(self):
        return f'<Season {self.season_name} {self.start_date} {self.end_date}>'

class EventType(db.Model):
    """
    example event_type add to db:

    new_event_type = EventType(event_type_name='Rally')
    """
    id:                 so.Mapped[int] = so.mapped_column(primary_key=True)
    event_type_name:    so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    events: so.Mapped[list["Event"]] = so.relationship("Event", back_populates="event_type")

    def __repr__(self):
        return f'<EventType {self.event_type_name}>'

#region Driver, Event, Car Branch
class Driver(db.Model):
    """
    example driver add to db:

    new_driver = Driver(driver_name='John Doe')
    db.session.add(new_driver)
    db.session.commit()
    
    """
    id:             so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_name:    so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    driver_events:  so.Mapped[list["DriverEvent"]] = so.relationship("DriverEvent", back_populates="driver")

    def __repr__(self):
        return f'<Driver {self.driver_name}>'
    
    def get_slug(self):
        return slugify(self.driver_name)
    
class Event(db.Model):
    """
    example event add to db:

    new_event = Event(event_name='Grand Prix', event_date=date(2024, 4, 1))
    db.session.add(new_event)
    db.session.commit()
    """

    id:             so.Mapped[int] = so.mapped_column(primary_key=True)
    event_name:     so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    event_date:     so.Mapped[datetime.date] = so.mapped_column(sa.Date, index=True)
    event_type_id:  so.Mapped[int] = so.mapped_column(sa.ForeignKey('event_type.id'), index=True)
    season_id:      so.Mapped[int] = so.mapped_column(sa.ForeignKey('season.id'), index=True)

    event_type:     so.Mapped["EventType"] = so.relationship("EventType", back_populates="events")
    season:         so.Mapped["Season"] = so.relationship("Season", back_populates="events")
    
    driver_events:  so.Mapped[list["DriverEvent"]] = so.relationship("DriverEvent", back_populates="event")

    # init method to auto assign season_id based on Event's event_date
    def __init__(self, event_name, event_date, event_type_id, **kwargs):
        super().__init__(**kwargs)
        self.event_name = event_name
        self.event_date = event_date
        self.event_type_id = event_type_id

        # Automatically assign season_id based on event_date
        season = Season.query.filter(
            Season.start_date <= event_date,
            Season.end_date >= event_date
        ).first()
        if not season:
            raise ValueError(f"No season found for event_date {event_date}.")
        self.season_id = season.id

    def __repr__(self):
        return f'<Event: {self.event_name} {self.event_type} {self.season}>'
    
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
        return f'<Car name={self.car_name}, class={self.car_class}>'
#endregion

#region DriverEvent Branch   
class DriverEvent(db.Model):
    """
    Association table to link drivers to events with unique cars and classes.

    example driver_event add to db:

    new_driverEvent = DriverEvent(driver_id=1, event_id=1, car_id=1)
        
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
    driver_event_stats: so.Mapped[Optional["DriverEventStats"]] = so.relationship("DriverEventStats", back_populates="driver_event")

    def __repr__(self):
        return f"<DriverEvent {self.driver}, {self.event}, {self.car}, {self.driver_event_stats}, {self.laptimes}>"
        
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

    fastest_lap:        so.Mapped[float] = so.mapped_column(sa.Float)
    average_lap:        so.Mapped[float] = so.mapped_column(sa.Float)
    total_laps:         so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    raw_time:           so.Mapped[float] = so.mapped_column(sa.Float)
    total_time:         so.Mapped[float] = so.mapped_column(sa.Float)

    driver_event:       so.Mapped["DriverEvent"] = so.relationship("DriverEvent", back_populates="driver_event_stats")

    def __repr__(self):
        return f'<DriverEventStats fastest_lap={self.fastest_lap} average_lap={self.average_lap} total_laps={self.total_laps}>'

class Laptime(db.Model):
    """
    example laptime add to db:

    new_laptime = Laptime(driver_event_id=1, laptime=timedelta(minutes=1, seconds=30), run_number=1)

    db.session.add(new_laptime)
    db.session.commit()
    """
    id:                 so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_event_id:    so.Mapped[int] = so.mapped_column(sa.ForeignKey('driver_event.id'))
    
    laptime:            so.Mapped[float] = so.mapped_column(sa.Float)
    run_number:         so.Mapped[int] = so.mapped_column(sa.Integer, index=True)

    driver_event:       so.Mapped["DriverEvent"] = so.relationship("DriverEvent", back_populates="laptimes")

    def __repr__(self):
        return f'<Laptime run={self.run_number} time={self.laptime}>'
#endregion


#region DriverSeasonStats Branch
class DriverSeasonStats(db.Model):
    """
    example driver_season_stats add to db:

    new_driver_season_stats = DriverSeasonStats(driver_id=1, season_id=1)
    """

    id:             so.Mapped[int] = so.mapped_column(primary_key=True)
    driver_id:      so.Mapped[int] = so.mapped_column(sa.ForeignKey('driver.id'), index=True)
    season_id:      so.Mapped[int] = so.mapped_column(sa.ForeignKey('season.id'), index=True)

    total_events:   so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    total_points:   so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
 



#endregion

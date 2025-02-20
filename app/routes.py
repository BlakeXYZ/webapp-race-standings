from flask import render_template
import sqlalchemy as sa
from app import app, db

from app.models import Driver, Event

@app.route('/')
@app.route('/home')
def my_home():
    return render_template('home.html', title='Home')

@app.route('/about')
def my_about():
    return render_template('about.html', title='About')

@app.route('/style-guide')
def my_style_guide():
    return render_template('style_guide.html', title='About')


@app.route('/driver/<slug>-<int:driver_id>')
def driver(driver_id, slug):
    driver = db.first_or_404(sa.select(Driver).where(Driver.id == driver_id))
    return render_template('driver.html', driver=driver)

@app.route('/event/<int:year>/<int:event_id>')
def event(year, event_id):
    event = db.first_or_404(sa.select(Event).where(Event.id == event_id, sa.extract('year', Event.event_date) == year))
    return render_template('event.html', event=event)
    
    

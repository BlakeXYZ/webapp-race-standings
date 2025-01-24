from flask import render_template
import sqlalchemy as sa
from app import app, db

from app.models import Driver, Event

@app.route('/')
@app.route('/index')
def my_index():

    user = {'username': 'Miguel'}
    event_list = ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5']
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts, event_list=event_list)

@app.route('/about')
def my_about():
    return render_template('about.html', title='About')

@app.route('/driver/<driver_name>')
def driver(driver_name):

    # driver_post = {
    #     'driver': driver,
    #     'driver_post': 'This is a post from the driver.' 
    # }

    driver = db.first_or_404(sa.select(Driver).where(Driver.driver_name == driver_name))
    
    return render_template('driver.html', driver=driver)

@app.route('/event/<int:event_id>')
def event(event_id):
    event = db.first_or_404(sa.select(Event).where(Event.id == event_id))

    return render_template('event.html', event=event)
    
    

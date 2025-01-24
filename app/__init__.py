from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import sqlalchemy as sa


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from app import routes, models 
from app.models import Driver, Event

#TODO: Find better home for global variables and init functions
#TODO: Setup Nav Bar Drop Down menus: Current Season DropDown + Archived Seasons DropDown
@app.context_processor
def inject_globals():
    drivers = db.session.scalars(sa.select(Driver)).all()
    events = db.session.scalars(sa.select(Event)).all()
    return {
        'drivers': drivers,
        'events': events
    }
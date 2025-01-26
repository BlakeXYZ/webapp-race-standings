from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler

import os
import sqlalchemy as sa


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


from app import routes, models, errors
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
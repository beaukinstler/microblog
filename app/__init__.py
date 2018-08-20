from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

"""
The database is going to be represented in the application by the database
instance. The database migration engine will also have an instance. These are
objects that need to be created after the application,
"""
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models

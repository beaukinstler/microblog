from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

"""
The database is going to be represented in the application by the database
instance. The database migration engine will also have an instance. These are
objects that need to be created after the application,
"""
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models   # noqa

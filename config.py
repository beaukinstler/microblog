import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    json_key = ''
    database_url_key = ''
    with open('secrets/secrets.json', 'r') as json_file:
        json_data = json.loads(json_file.read())
        try:
            json_key = json_data['super_secret_key']
        except:
            pass
        try:
            database_url_key = json_data['database_url']
        except:
            pass

    SUPER_SECRET_KEY = os.environ.get('SUPER_SECRET_KEY') or json_key
    # Flask requires a constant call "SECRET_KEY", so I'm setting two
    # In other projects I plan to adapt to this, I've used SUPER_ so I'm
    # just keeping both as an option, so that both can be used, but 
    # it will be the same key. 
    SECRET_KEY = SUPER_SECRET_KEY

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db') or \
            database_url_key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
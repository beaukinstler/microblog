import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    json_key = ''
    with open('secrets/secrets.json', 'r') as json_file:
        json_key = json.loads(json_file.read())['super_secret_key']
    SUPER_SECRET_KEY = os.environ.get('SUPER_SECRET_KEY') or json_key
    # Flask requires a constant call "SECRET_KEY", so I'm setting two
    # In other projects I plan to adapt to this, I've used SUPER_ so I'm
    # just keeping both as an option, so that both can be used, but 
    # it will be the same key. 
    SECRET_KEY = SUPER_SECRET_KEY
    
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            ('sqlite:///' + os.path.join(basedir, 'app.db'))
    
    """
    Do not use the TRACK MODIFICATIONS to send a signal to the app
    when a database change is about to be made
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MP3DIR = 'static/mp3s'
    KEEPMP3S = False

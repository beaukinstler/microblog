import os
from dotenv import load_dotenv
# import json

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """
    Purpose:    used for setting variable, found in the environment, or pulled
                from the secrets file.
                Preference is given the the 'secrets/secrets.json' file.
    """


    # the other keys default to the json file.  This secret goes back to
    # to defering to the OS Environment instead.  Add similar logic to
    # do the same for other keys
    SUPER_SECRET_KEY = os.environ.get('SUPER_SECRET_KEY')

    # Flask requires a constant call "SECRET_KEY", so I'm setting two
    # In other projects I plan to adapt to this, I've used `SUPER_` so I'm
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

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    #  Pagination
    POSTS_PER_PAGE = 25

    LANGUAGES = ['en', 'es']

    # Elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

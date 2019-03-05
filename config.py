import os
import re
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """
    Purpose:    used for setting variable, found in the environment
    """
    APP_NAME = os.environ.get('APP_NAME') or 'Generic App -- change this in config.py'  # noqa
    APP_NAME_SNAKE = re.sub("[ ]", "_", APP_NAME).lower()
    SUPER_SECRET_KEY = os.environ.get('SUPER_SECRET_KEY')  # for Google API
    SECRET_KEY = os.environ.get('SECRET_KEY')  # flask
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        ('sqlite:///' + os.path.join(basedir, 'app.db'))

    TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or \
        ('sqlite:///' + os.path.join(basedir, 'test_app.db'))

    # OTHERS/MISC
    """
    Do not use the TRACK MODIFICATIONS to send a signal to the app
    when a database change is about to be made
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en']

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    MS_TRANSLATE_KEY = os.environ.get('MS_TRANSLATE_KEY')

    #  Pagination
    POSTS_PER_PAGE = 25

    LANGUAGES = ['en', 'es']

    # Elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

import os
from dotenv import load_dotenv
import json

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """
    Purpose:    used for setting variable, found in the environment, or pulled
                from the secrets file.
                Preference is given the the 'secrets/secrets.json' file.
    """
    json_key = ''
    mail_server = ''
    mail_port = ''
    mail_uses_tls = ''
    mail_username = ''
    mail_password = ''
    admin_email = ''

    with open('secrets/secrets.json', 'r') as json_file:
        json_blob = json.loads(json_file.read())

        try:
            json_key = json_blob['super_secret_key']
        except Exception as e:
            json_key = os.environ.get('SUPER_SECRET_KEY')

        try:
            mail_server = json_blob['mail_server']
        except Exception as e:
            mail_server = os.environ.get('MAIL_SERVER')

        try:
            mail_port = json_blob['mail_port']
        except Exception as e:
            mail_port = os.environ.get('MAIL_PORT')

        try:
            mail_uses_tls = json_blob['mail_uses_tls']
        except Exception as e:
            mail_uses_tls = os.environ.get('MAIL_USE_TLS')

        try:
            mail_username = json_blob['mail_username']
        except Exception as e:
            mail_username = os.environ.get('MAIL_USERNAME')

        try:
            mail_password = json_blob['mail_password']
        except Exception as e:
            mail_password = os.environ.get('MAIL_PASSWORD')

        try:
            admin_email = json_blob['admin_email']
        except Exception as e:
            admin_email = os.environ.get('ADMIN_EMAIL')

    # the other keys default to the json file.  This secret goes back to
    # to defering to the OS Environment instead.  Add similar logic to
    # do the same for other keys
    SUPER_SECRET_KEY = os.environ.get('SUPER_SECRET_KEY') or json_key

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

    MAIL_SERVER = mail_server or 'localhost'
    MAIL_PORT = int(mail_port or 25)
    MAIL_USE_TLS = mail_uses_tls is not None
    MAIL_USERNAME = mail_username
    MAIL_PASSWORD = mail_password
    ADMIN_EMAIL = admin_email

    #  Pagination
    POSTS_PER_PAGE = 25

    LANGUAGES = ['en', 'es']

    # Elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

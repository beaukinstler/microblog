import os
import json

class Config(object):
    json_key = ''
    with open('secrets/secrets.json', 'r') as json_file:
        json_key = json.loads(json_file.read())['super_secret_key']
    SUPER_SECRET_KEY = os.environ.get('SUPER_SECRET_KEY') or json_key
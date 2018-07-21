import os
import json

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
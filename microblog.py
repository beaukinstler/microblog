from app import app
import json


SUPER_SECRET_KEY = (
        json.loads(
            open('secrets/secrets.json', 'r')
            .read())['super_secret_key']
    )


if __name__ == '__main__':
    app.secret_key = SUPER_SECRET_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
from app import app, db
from app.models import User, Post, Denial
import json
from app import cli
import app.civic as civic

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Denial': Denial, 'civic': civic}


SUPER_SECRET_KEY_OLD = (
        json.loads(
            open('secrets/secrets.json', 'r')
            .read())['super_secret_key']
    )


if __name__ == '__main__':
    app.secret_key = app.config['SUPER_SECRET_KEY']
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
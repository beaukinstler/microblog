from app import create_app, db, cli
from app.models import User, Post
import json

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    app.secret_key = app.config['SUPER_SECRET_KEY']
    app.debug = True
    app.run(host='0.0.0.0', port=8080)

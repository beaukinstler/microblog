from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

from app import login, app
from jwt import encode, decode
from time import time


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


"""
Linking tables:
These links are only that, and hold no data in this model.

in flask, in order to use the migrations for these tables, we'll
run commands such as...
`$ flask db migrate -m 'followers'`
`$ flask db upgrade `
"""
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


favorites_tbl = db.Table(
    'favorites',
    db.Column('fan_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('favorite_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    favorited = db.relationship(
            'User', secondary=favorites_tbl,
            primaryjoin=(favorites_tbl.c.fan_id == id),
            secondaryjoin=(favorites_tbl.c.favorite_id == id),
            backref=db.backref('fans', lazy='dynamic'), lazy='dynamic'
    )
    followed = db.relationship(
            'User', secondary=followers,
            primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),
            backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        """
        The __repr__ method tells Python how to print objects of this class,
        which is going to be useful for debugging.
        For user with username susan, it will look like "<User susan>"
        """
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def add_favorite(self, user):
        if not self.is_favorite(user):
            self.favorited.append(user)

    def remove_favorite(self, user):
        if self.is_favorite(user):
            self.favorited.remove(user)

    def is_favorite(self, user):
        return self.favorited.filter(
            favorites_tbl.c.favorite_id == user.id).count() > 0

    def followed_posts(self):
        followed_posts = Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)).\
            filter(followers.c.follower_id == self.id)
        own_posts = Post.query.filter_by(user_id=self.id)
        return followed_posts.union(own_posts).order_by(Post.timestamp.desc())

    def favorite_posts(self):
        fav_posts = Post.query.join(
            favorites_tbl,
            (favorites_tbl.c.favorite_id == Post.user_id)).\
            filter(favorites_tbl.c.fan_id == self.id)
        return fav_posts.order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = decode(token, app.config['SECRET_KEY'],
                        algorithms=['HS256'])['reset_password']
        except Exception as e:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

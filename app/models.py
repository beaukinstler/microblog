from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    
    def __repr__(self):
        """
        The __repr__ method tells Python how to print objects of this class,
        which is going to be useful for debugging.
        For user with username susan, it will look like "<User susan>"
        """
        return '<User {}>'.format(self.username)    
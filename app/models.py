from datetime import datetime
from app import db

# moduel of user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Relation to Post moduel
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # The __repr__ method tells Python how to print objects of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)


# moduel of post table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(150))
    # timestamp arg default passing the function itself, not the result.
    # mention the utcnow
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # mention the usage of ForeigneKey
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
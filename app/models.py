from datetime import datetime
from app import db
# for user login function
from app import login
# These two functions are used to change the password to hash and check it
from werkzeug.security import generate_password_hash, check_password_hash
# for login function
from flask_login import UserMixin
# for user avatar
from hashlib import md5
# password reset validation
from time import time
import jwt
from app import app

# a many-to-many relation
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# module of user table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Relation to Post module
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # New function of self-introduction
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # Remember, Every time the database is modified ,
    # it is necessary to generate a database migration.
    # $ flask db migrate -m "some comments..."
    # $ flask db upgrade

    # auxiliary table
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # The __repr__ method tells Python how to print objects of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # The whole password hashing logic can be implemented as two new methods in the user model:
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # If the password is correct ,then return True
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Generate avatar
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # functions of following
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        # Note how the followed and own queries are combined into one
        return followed.union(own).order_by(Post.timestamp.desc())

    # Password reset
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

# return unique user id
# The user loader is registered with Flask-Login with the @login.user_loader decorator.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


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


from . import db
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime

class Film(db.Model):
    __tablename__='films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    poster = db.Column(db.String(256))
    description = db.Column(db.String(256))
    is_series = db.Column(db.Boolean)
    score = db.relationship('Score', backref='film', lazy='dynamic')
    film_allocation = db.relationship('Film_allocation', backref='film', lazy='dynamic')

class Score(db.Model):
    __tablename__='score'
    id = db.Column(db.Integer, primary_key=True)
    filmscore = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'))

class Actors(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    film_allocation = db.relationship('Film_allocation', backref='actor', lazy='dynamic')

class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    film_allocation = db.relationship('Film_allocation', backref='director', lazy='dynamic')

class Film_allocation(db.Model):
    __tablename__='film_allocation'
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('films.id'),primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'),primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'),primary_key=True)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    film = db.relationship('Score', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):  # hashing the password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # checking password that someone gave with that in database
        return check_password_hash(self.password_hash, password)

    # confirm your email
    def generate_confirmation_token(self, expiration=3600):  # generating token for account confirmation
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):       #confirmation of account
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):    #generating token to reset password
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset':self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):  # reseting password
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):  # generating token to change email
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email

        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from . import db
from . import bcrypt
from flask_login import login_manager, UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30),
                         nullable=False, unique=True)
    password_hash = db.Column(db.String(length=100),
                              nullable=False)
    bookmarks = db.relationship('Bookmark', backref='owner', lazy=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = bcrypt.generate_password_hash(
            value).decode('utf-8')

    def check_password(self, input_password):
        return bcrypt.check_password_hash(self.password_hash, input_password)

    def __repr__(self):
        return f'User ID: {self.id}, username: {self.username}'


class Bookmark(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    anime_id = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id'), nullable=True, default=None)

    def __repr__(self):
        return f'Anime ID: {self.anime_id}'

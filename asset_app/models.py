from flask import app
from asset_app import db, login_manager
from asset_app import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Asset(db.Model):

    # __bind_key__='one'
    # __bind_key__='two'

    asset_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    criticality = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'Asset {self.name}'


class User(db.Model, UserMixin):

    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    pwd = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        return self.pwd

    @password.setter
    def password(self, plain_text_password):
        self.pwd = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.pwd, attempted_password)

    def get_id(self):
        return self.user_id

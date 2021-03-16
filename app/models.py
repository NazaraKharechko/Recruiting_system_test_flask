from app import db
from flask_login import UserMixin


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'id = {self.id} email = {self.email}'


class Positions(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    positions = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(350), nullable=False)

    def __repr__(self):
        return f'id = {self.id} positions = {self.positions} {self.description}'


class CV_model(db.Model):
    __tablename__ = 'cv'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    cv = db.Column(db.String(50), default='cv netu')
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id', ondelete='CASCADE'), nullable=False, default='1')

    def __repr__(self):
        return f'id = {self.id} positions = {self.name}'


class RecruiterModel(db.Model):
    __tablename__ = 'recruiter'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    profession = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    candidates = db.relationship('CV_model', backref='recruiter')

    def __repr__(self):
        return f'name => {self.name} profession => {self.profession}'

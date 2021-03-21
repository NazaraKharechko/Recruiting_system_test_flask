from app import db
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash,  check_password_hash
import hashlib


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'id = {self.id} email = {self.email}'

    # def __init__(self):
    #     h = hashlib.md5(selfpassword.encode())
    #     h.hexdigest()


class Positions(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    positions = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(350), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'id = {self.id} positions = {self.positions} {self.end_date}'

    @classmethod
    def del_data(cls):
        tims_now = datetime.datetime.now()
        data = tims_now.strftime('%Y-%m-%d %H:%M:00')
        if data >= cls.end_date:
            print(cls.end_date)
            db.session.delete(self.id)
            db.session.commit()


class CV_model(db.Model):
    __tablename__ = 'cv'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    cv = db.Column(db.String(50), default='cv netu')
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id', ondelete='CASCADE'), nullable=False,
                             default=1 or 2)
    interview = db.relationship('InterviewModel', backref='candidates', lazy=True)

    def __repr__(self):
        return f'id = {self.id} positions = {self.name}'


class RecruiterModel(db.Model, UserMixin):
    __tablename__ = 'recruiter'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    profession = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    candidates = db.relationship('CV_model', backref='recruiter')
    interview = db.relationship('InterviewModel', backref='recruiter', lazy=True)

    def __repr__(self):
        return f'name => {self.name} profession => {self.profession}'

    def __init__(self):
        h = hashlib.md5(selfpassword.encode())
        h.hexdigest()


class InterviewModel(db.Model):
    __tablename__ = 'interview'
    id = db.Column(db.Integer, primary_key=True)

    interview_date = db.Column(db.DateTime())
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'),
                             nullable=False)
    candidates_id = db.Column(db.Integer, db.ForeignKey('cv.id'),
                              nullable=False)

    def __repr__(self):
        return f'data => {self.interview_date}'

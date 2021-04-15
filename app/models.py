from app import db
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, mapper


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'user',
    #     'polymorphic_on': user_type
    # }

    def __repr__(self):
        return f'id = {self.id} email = {self.email}'

    def __init__(self, *args, **kwargs):
        password = kwargs.pop("password")
        password_hash = generate_password_hash(password)
        super().__init__(password=password_hash, *args, **kwargs)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Positions(db.Model):
    __tablename__ = 'positions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    positions = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(350), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    candidate = db.relationship('CVS_model', uselist=False, backref='position')

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


class CVS_model(db.Model):
    __tablename__ = 'cvs'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    cv = db.Column(db.String(50), default='cv netu')

    position_id = db.Column(db.Integer, db.ForeignKey('positions.id', ondelete='CASCADE'))

    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id', ondelete='CASCADE'), nullable=False)
    interview = db.relationship('InterviewModel', backref='candidates', lazy=True)
    reject = db.relationship('RejectModel', backref='candidates_reject', lazy=True)

    def __repr__(self):
        return f'id = {self.id} name = {self.name} '


class RecruiterModel(db.Model, UserMixin):
    __tablename__ = 'recruiter'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    profession = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    candidates = db.relationship('CVS_model', backref='recruiter')
    interview = db.relationship('InterviewModel', backref='recruiter', lazy=True)

    def __repr__(self):
        return f' id => {self.id} name => {self.name} profession => {self.profession}'

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password')
        password_hash = generate_password_hash(password)
        super().__init__(password=password_hash, *args, **kwargs)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class InterviewModel(db.Model):
    __tablename__ = 'interview'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    interview_date = db.Column(db.DateTime())
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'),
                             nullable=False)
    candidates_id = db.Column(db.Integer, db.ForeignKey('cvs.id'),
                              nullable=False)

    def __repr__(self):
        return f'data => {self.interview_date}'


class RejectModel(db.Model):
    __tablename__ = 'reject'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    candidates_id = db.Column(db.Integer, db.ForeignKey('cvs.id'),
                              nullable=False)
    why = db.Column(db.String(200))
    chek = db.Column(db.Boolean())

    def __repr__(self):
        return f'who => {self.candidates_id} why > {self.why}'







# __mapper_args__ = {
#     'polymorphic_identity': 'user',
#     # 'polymorphic_on': user_type
# }

# __table_args__ = {'extend_existing': True}
# __mapper_args__ = {
#     'polymorphic_identity': 'recruiter',
# }
# def __repr__(self):
#     return ' '.join([super().__repr__(), f' id => {self.id} name => {self.name} profession => {self.profession}'])
#

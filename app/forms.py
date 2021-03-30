from wtforms import Form, StringField, PasswordField, SubmitField, FileField, BooleanField, SelectField
from wtforms.validators import DataRequired, length, Email, EqualTo
from .models import RecruiterModel, CV_model


class RegisterForm(Form):
    email = StringField('Email', [DataRequired(), length(3, 30, 'Email must be 3-30 characters')])
    password = PasswordField('Password', [DataRequired(), length(6, 20, 'Password must be 6-20 characters')])
    confirm = PasswordField('Confirm', [DataRequired(), EqualTo('password', 'Passwords is not equals'),
                                        length(6, 20, 'Password must be 6-20 characters')])
    register = SubmitField('Register')


class LoginForm(Form):
    email = StringField('Email', [DataRequired(), length(3, 30, 'Email must be 3-30 characters')])
    password = PasswordField('Password', [DataRequired(), length(6, 20, 'Password must be 6-20 characters')])
    login = SubmitField('Login')


class Send_cv_Form(Form):
    choices = [('Python', 'Python'),
               ('JS', 'JS'),
               ('Html', 'Html'),
               ('Python 3+', 'Python 3+'),
               ('Vu.js', 'Vu.js')]
    email = StringField('Email', [DataRequired(), length(3, 30, 'Email must be 3-30 characters')])
    name = StringField('Name')
    age = StringField('Age')
    stek = SelectField(choices=choices)

    cv = FileField('Cv')
    send = SubmitField('Send')


class Positions_Create_Form(Form):
    positions = StringField('Positions')
    description = StringField('Description')
    start_date = StringField('Start_date')
    end_date = StringField('End_date')
    create = SubmitField('Create')


class Positions_Delete_Form(Form):
    id_delete = StringField('Id_delete')
    delete = SubmitField('Delete')


class Reject_Form(Form):
    candidates_id = StringField('Сandidates_id')
    why = StringField('Why')
    chek = BooleanField('Chek')
    reject = SubmitField('Reject')


class Create_Interview_Form(Form):
    rek = RecruiterModel.query.all()
    us = CV_model.query.all()
    for i in rek:
        choices_interview = [(i.id, i.profession)]
        interview_date = StringField('Interview_date')
        recruiter_id = SelectField(choices=choices_interview)
    for u in us:
        choices_users = [(u.id, u.stek)]
        candidates_id = SelectField(choices=choices_users)
        create = SubmitField('Create')


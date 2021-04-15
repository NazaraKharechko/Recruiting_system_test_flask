from wtforms import Form, StringField, PasswordField, SubmitField, FileField, BooleanField, SelectField
from wtforms.validators import DataRequired, length, Email, EqualTo
from .models import RecruiterModel, CVS_model, Positions
from wtforms_sqlalchemy.fields import QuerySelectField


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
    # choices = [('Python', 'Python'),
    #            ('JS', 'JS'),
    #            ('Html', 'Html'),
    #            ('Python 3+', 'Python 3+'),
    #            ('Vu.js', 'Vu.js')]
    email = StringField('Email', [DataRequired(), length(3, 30, 'Email must be 3-30 characters')])
    name = StringField('Name')
    age = StringField('Age')
    # stek = SelectField(choices=choices)

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
    users_id = QuerySelectField(query_factory=CVS_model.query.all)
    # candidates_id = SelectField(choices=choices_users)

    why = StringField('Why')
    chek = BooleanField('Chek')
    reject = SubmitField('Reject')


class Create_Interview_Form(Form):
    choices_interview = [(g.id, [g.id, g.name, g.profession]) for g in RecruiterModel.query.all()]
    recruiter_id = SelectField(choices=choices_interview)
    choices_users = [(g.id, [g.id, g.name, Positions.query.filter_by(id=g.position_id).first().positions]) for g in
                     CVS_model.query.all()]
    candidates_id = SelectField(choices=choices_users)
    interview_date = StringField('Interview_date')
    create = SubmitField('Create')

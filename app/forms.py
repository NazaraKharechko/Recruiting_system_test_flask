from wtforms import Form, StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, length, Email, EqualTo


class RegisterForm(Form):
    email = StringField('Email', [DataRequired(),  length(3, 30, 'Email must be 3-30 characters')])
    password = PasswordField('Password', [DataRequired(), length(6, 20, 'Password must be 6-20 characters')])
    confirm = PasswordField('Confirm', [DataRequired(), EqualTo('password', 'Passwords is not equals'),
                                        length(6, 20, 'Password must be 6-20 characters')])
    register = SubmitField('Register')


class LoginForm(Form):
    email = StringField('Email', [DataRequired(),  length(3, 30, 'Email must be 3-30 characters')])
    password = PasswordField('Password', [DataRequired(), length(6, 20, 'Password must be 6-20 characters')])
    login = SubmitField('Login')


class Send_cv_Form(Form):
    email = StringField('Email', [DataRequired(),  length(3, 30, 'Email must be 3-30 characters')])
    name = StringField('Name')
    age = StringField('Age')
    cv = FileField('Cv')
    send = SubmitField('Send')
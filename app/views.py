from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegisterForm, Send_cv_Form
from app.models import UserModel, Positions, CV_model, InterviewModel
import datetime


@app.route('/')
def home():
    return redirect('positions')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate = UserModel.query.filter_by(email=form.email.data).first()
        print(candidate)
        if candidate and candidate.password == form.password.data:
            login_user(candidate)
            return redirect('admin')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        del data['confirm']
        del data['register']
        email = UserModel.query.filter_by(email=data['email']).first()
        if email:
            return render_template('register.html', form=form, error='Email is already exist')
        user = UserModel(**data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/positions')
def positions():
    position = Positions.query.all()
    return render_template('positions.html', position=position)


@app.route('/cv', methods=['GET', 'POST'])
def cv():
    form = Send_cv_Form(request.form)
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        del data['send']
        cv = CV_model(**data)
        db.session.add(cv)
        db.session.commit()
        return redirect(url_for('positions'))
    return render_template('cv.html', form=form)


@app.route('/interview')
def interview():
    interview = InterviewModel.query.all()
    print(interview)
    return render_template('interview.html', interview=interview)

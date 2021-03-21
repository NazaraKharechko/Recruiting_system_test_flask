from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.forms import LoginForm, RegisterForm, Send_cv_Form, Positions_Create_Form, Positions_Delete_Form, \
    Create_Interview_Form
from app.models import UserModel, Positions, CV_model, InterviewModel, RecruiterModel
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
        return redirect(url_for('home'))
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
    email = current_user.email
    id = UserModel.query.filter_by(email=email).first()
    print(id.id)
    interview = InterviewModel.query.filter_by(candidates_id=id.id).first()
    print(interview)
    return render_template('interview.html', interview=interview)


@app.route('/login/users', methods=['GET', 'POST'])
def login_users():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate = UserModel.query.filter_by(email=form.email.data).first()
        if candidate and candidate.password == form.password.data:
            login_user(candidate)
            return redirect('/my/cv')
    return render_template('login_users.html', form=form)


@app.route('/login/recruiter', methods=['GET', 'POST'])
def login_recruiter():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate = RecruiterModel.query.filter_by(email=form.email.data).first()
        if candidate and candidate.password == form.password.data:
            login_user(candidate)
            return redirect('/recruiter')
    return render_template('login_users.html', form=form)


@app.route('/my/cv')
def my_cv():
    email = current_user.email
    cvs = CV_model.query.filter_by(email=email).first()
    return render_template('my_cv.html', cvs=cvs, email=email)


@app.route('/recruiter', methods=['GET', 'POST'])
def recruiter():
    position = Positions.query.all()
    form = Positions_Create_Form(request.form)
    all_users = UserModel.query.all()
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        del data['create']
        pos = Positions(**data)
        db.session.add(pos)
        db.session.commit()
        return redirect(url_for('recruiter'))
    return render_template('recruiter.html', position=position, form=form, all_users=all_users)


@app.route('/delete/position', methods=['GET', 'POST'])
def delete_position():
    form = Positions_Delete_Form(request.form)
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        del data['delete']
        pos_d = Positions.query.filter_by(id=data['id_delete']).delete()
        db.session.commit()
        return redirect(url_for('recruiter'))
    return render_template('dalete.html', form=form)


@app.route('/create/interview', methods=['GET', 'POST'])
def create_interview():
    form = Create_Interview_Form(request.form)
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        print(data)
        del data['create']
        i = InterviewModel(**data)
        db.session.add(i)
        db.session.commit()
        return redirect(url_for('recruiter'))
    return render_template('create_interview.html', form=form)

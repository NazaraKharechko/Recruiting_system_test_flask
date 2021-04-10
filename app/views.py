from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.forms import LoginForm, RegisterForm, Send_cv_Form, Positions_Create_Form, Positions_Delete_Form, \
    Create_Interview_Form, Reject_Form
from app.models import UserModel, Positions, CVS_model, InterviewModel, RecruiterModel, RejectModel
import random


@app.route('/')
def home():
    render_template('base.html', current_user=current_user)
    return redirect('positions')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        candidate = UserModel.query.filter_by(email=form.email.data).first()
        recruiter = RecruiterModel.query.filter_by(email=form.email.data).first()
        if candidate and candidate.verify_password(form.password.data) and candidate.admin == False:
            login_user(candidate)
            return redirect('/my/cv')
        if recruiter and recruiter.verify_password(form.password.data):
            return redirect('/recruiter')
        if candidate and candidate.verify_password(form.password.data) and candidate.admin == True:
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
    return redirect(url_for('positions'))


@app.route('/positions')
def positions():
    position = Positions.query.all()
    return render_template('positions.html', position=position)


@app.route('/cv/<int:id_pos>', methods=['GET', 'POST'])
def cv(id_pos):
    form = Send_cv_Form(request.form)
    id_p = int(id_pos)
    r = RecruiterModel.query.all()
    random_recruiter_id = random.choice(r)
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        del data['send']
        cv = CVS_model(**data, position_id=id_p, recruiter_id=random_recruiter_id.id)
        db.session.add(cv)
        db.session.commit()
        return redirect(url_for('positions'))
    return render_template('cv.html', form=form)


@app.route('/interview')
def interview():
    email = current_user.email
    id = CVS_model.query.filter_by(email=email).first()
    interview = InterviewModel.query.filter_by(candidates_id=id.id)
    reject = RejectModel.query.filter_by(candidates_id=id.id).first()
    return render_template('interview.html', interview=interview, reject=reject)


# @app.route('/login/users', methods=['GET', 'POST'])
# def login_users():
#     form = LoginForm(request.form)
#     if request.method == 'POST' and form.validate():
#         candidate = UserModel.query.filter_by(email=form.email.data).first()
#         if candidate and candidate.password == form.password.data:
#             login_user(candidate)
#             return redirect('/my/cv')
#     return render_template('login_users.html', form=form)
#
#
# @app.route('/login/recruiter', methods=['GET', 'POST'])
# def login_recruiter():
#     form = LoginForm(request.form)
#     if request.method == 'POST' and form.validate():
#         candidate = RecruiterModel.query.filter_by(email=form.email.data).first()
#         if candidate and candidate.password == form.password.data:
#             login_user(candidate)
#             return redirect('/recruiter')
#     return render_template('login_users.html', form=form)


@app.route('/my/cv', methods=['GET', 'POST'])
def my_cv():
    email = current_user.email
    cvs = CVS_model.query.filter_by(email=email)
    return render_template('my_cv.html', cvs=cvs, email=email)


@app.route('/recruiter', methods=['GET', 'POST'])
def recruiter():
    position = Positions.query.all()
    form = Positions_Create_Form(request.form)
    all_users = CVS_model.query.all()
    all_reject_user = RejectModel.query.all()
    interview = InterviewModel.query.all()
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        del data['create']
        pos = Positions(**data)
        db.session.add(pos)
        db.session.commit()
        return redirect(url_for('recruiter'))
    return render_template('recruiter.html', position=position, form=form, all_users=all_users, interview=interview,
                           all_reject_user=all_reject_user)


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
        del data['create']
        profession = RecruiterModel.query.filter_by(id=data['recruiter_id'].id).first()
        stek = CVS_model.query.filter_by(id=data['candidates_id'].id).first()
        user_stek = stek.position_id
        users = Positions.query.filter_by(id=user_stek).first()
        if profession.profession >= users.positions:
            recruiter_id = data['recruiter_id'].id
            candidates_id = data['candidates_id'].id
            i = InterviewModel(recruiter_id=recruiter_id, candidates_id=candidates_id, **data)
            print(i)
            db.session.add(i)
            db.session.commit()
            return redirect(url_for('recruiter'))
        else:
            return """Profession recruiter does not match the stack user Go back?"""
    return render_template('create_interview.html', form=form)


@app.route('/reject_user', methods=['GET', 'POST'])
def reject_user():
    form = Reject_Form(request.form)
    if request.method == 'POST' and form.validate():
        data = dict(form.data)
        del data['reject']
        reject = RejectModel(**data)
        db.session.add(reject)
        db.session.commit()
        return redirect(url_for('recruiter'))
    return render_template('reject_user.html', form=form)


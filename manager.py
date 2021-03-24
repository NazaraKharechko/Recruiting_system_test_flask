from app.models import UserModel, RecruiterModel, Positions
from flask_script import Manager
from app import db, app

manager = Manager(app)


admin = {'email': 'admin@gmail.com',
         'password': 'admin2020', 'admin': 1}

recruiter = {'email': 'recruiter@gmail.com',
             'password': 'recruiter2020', 'name': 'Bob', 'profession': 'Js', 'status': 1}

positions = {'positions': 'Python',
             'description': 'Python — інтерпретована оcscscs', 'start_date': '2021-03-02 12:06:00',
             'end_date': '2021-05-02 12:06:00'}


@manager.command
def seed():
    db.session.add(UserModel(**admin))
    db.session.add(RecruiterModel(**recruiter))
    db.session.add(Positions(**positions))
    db.session.commit()


if __name__ == '__main__':
    manager.run()

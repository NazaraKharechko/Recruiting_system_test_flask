from .models import UserModel, RecruiterModel, Positions

admin = {'id': 1, 'email': 'admin@gmail.com',
         'password': 'admin2020', 'admin': 1}

recruiter = {'id': 1, 'email': 'admin@gmail.com',
             'password': 'admin2020', 'name': 'Bob', 'profession': 'Js', 'status': 1}

positions = {'id': 1, 'positions': 'Python',
             'description': 'Python — інтерпретована оcscscs', 'start_date': '2021-03-02 12:06:00',
             'end_date': '2021-05-02 12:06:00'}


admin = UserModel(**admin)
recruiter = RecruiterModel(**recruiter)
positions = Positions(**positions)


@manager.command
def seed():
    db.session.add(admin, recruiter, positions)
    db.session.commit()

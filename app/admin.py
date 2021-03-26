from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import current_user, LoginManager
from app import app, db
from app.models import UserModel, Positions, CV_model, RecruiterModel, InterviewModel, RejectModel


class MyModelView(ModelView):
    pass


class MySecureModelView(MyModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class MyAdminIndexViews(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


admin = Admin(app, index_view=MyAdminIndexViews())
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)


admin.add_view(MySecureModelView(UserModel, db.session))
admin.add_view(MySecureModelView(Positions, db.session))
admin.add_view(MySecureModelView(CV_model, db.session))
admin.add_view(MySecureModelView(RecruiterModel, db.session))
admin.add_view(MySecureModelView(InterviewModel, db.session))
admin.add_view(MySecureModelView(RejectModel, db.session))
admin.add_link(MenuLink('LogOut', '/positions'))



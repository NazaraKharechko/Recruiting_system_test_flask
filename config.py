class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/flask_recruiting_system'
    SECRET_KEY = 'YR}?J=bAE57XTr^T_gD=Jb^8?*?Y&-=qjw9}d#4d"&ZhE4'


class DevConfig(Config):
    DEBUG = True

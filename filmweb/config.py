import os



basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
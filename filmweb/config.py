import os



basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
                   ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'test.mail25741@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'test12345/'
    URLOPY_MAIL_SUBJECT_PREFIX = '[Filmweb]'
    URLOPY_MAIL_SENDER = "test.mail25741@gmail.com"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    TEMPLATES_AUTO_RELOAD = True
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
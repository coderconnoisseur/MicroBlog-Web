import os


basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'you-will-never-guess-it'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URI') or 'sqlite:///'+ os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3
    
    MAIL_SERVER='localhost'#or os.environ.get('MAIL_SERVER')
    MAIL_PORT=8025#int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS=False#os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = None#os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = None#os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
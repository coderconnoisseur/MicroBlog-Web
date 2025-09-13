import os


basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'you-will-never-guess-it'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URI') or 'sqlite:///'+ os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3
    
    MAIL_SERVER=None  # Disable mail server for development to prevent SMTP errors
    MAIL_PORT=None    # Disable mail port
    MAIL_USE_TLS=False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    ADMINS = ['your-email@example.com']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    
    # Rate Limiting Configuration
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_DEFAULT = "1000 per day, 100 per hour"
    RATELIMIT_HEADERS_ENABLED = True
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from elasticsearch import Elasticsearch

app = Flask(__name__ )
app.config.from_object(Config)
moment=Moment(app)
bootstrap = Bootstrap(app)
db =SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view='login'
mail=Mail(app)

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[app.config.get('RATELIMIT_DEFAULT', "1000 per day, 100 per hour")],
    storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://'),
    headers_enabled=app.config.get('RATELIMIT_HEADERS_ENABLED', True)
)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
if app.config['ELASTICSEARCH_URL'] else None
from Projectdir import routes,models,errors

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth=None
        if app.config['MAIL_USERNAME'] or app.config["MAIL_PASSWORD"]:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        secure=None
        if app.config['MAIL_USE_TLS']:
            secure=()
        mail_handler=SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"],app.config["MAIL_PORT"]),
            fromaddr='no-reply'+app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],subject='MICROBLOG FAILURE',
            credentials=auth,secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    # Add file logging as fallback for development
    import os
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
        
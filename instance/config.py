# myServer/instance/config.py

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EYECATCH='INSTANCE'
EXECUTION_MODE = 'sandbox'
EXECUTION_ENVIRONMENT = 'pythonanywhere'

MAIL_SERVER_PROVIDER = 'yandex'
MAIL_SERVER_PROVIDER = 'mailjet'
MAIL_SERVER_PROVIDER = 'google'
DEBUG = True
if MAIL_SERVER_PROVIDER=='mailjet':
    # email server mailjet
    os.environ["MAIL_SERVER"] = "in-v3.mailjet.com"
    #Port 25 or 587 (some providers block port 25). If TLS on port 587 doesn't work, try using port 465 and/or using SSL instead
    os.environ["MAIL_PORT"] = "587"
    os.environ["MAIL_USE_TLS"] = "True"
    os.environ["MAIL_USE_SSL"] = "True"
    os.environ["MAIL_USERNAME"] = "f8d33207c3c7a1ecaf2f74e809b57786"
    os.environ["MAIL_PASSWORD"] = "2d6a3c2de41ff45b5435382f3e267580"
    os.environ['MAIL_APIKEY_PUBLIC']='f8d33207c3c7a1ecaf2f74e809b57786'
    os.environ['MAIL_APIKEY_PRIVATE']='2d6a3c2de41ff45b5435382f3e267580'
else:
    if MAIL_SERVER_PROVIDER=='yandex':
        # email server yandex
        os.environ["MAIL_SERVER"] = "smtp.yandex.ru"
        os.environ["MAIL_PORT"] = "587"
        os.environ["MAIL_USE_TLS"] = "True"
        os.environ["MAIL_USE_SSL"] = "True"
        os.environ["MAIL_USERNAME"] = "........" #without the @yandex.ru
        os.environ["MAIL_PASSWORD"] = "********"
        os.environ['MAIL_APIKEY_PUBLIC']='...'
        os.environ['MAIL_APIKEY_PRIVATE']='...'
    else:
        # email server google
        os.environ["MAIL_SERVER"] = "smtp.gmail.com"
        os.environ["MAIL_PORT"] = "587"
        os.environ["MAIL_USE_TLS"] = "False"
        os.environ["MAIL_USE_SSL"] = "True"
        os.environ["MAIL_USERNAME"] = "akamas2020@gmail.com"
        os.environ["MAIL_PASSWORD"] = "philea13"
        os.environ["MAIL_USERNAME"] = "bstarr131@gmail.com"
        os.environ["MAIL_PASSWORD"] = "bstarr13"
        os.environ["MAIL_USERNAME"] = "akamas2020@gmail.com"
        os.environ["MAIL_PASSWORD"] = "philea13"
        os.environ["MAIL_USERNAME"] = "spithas@leandrou.com"
        os.environ["MAIL_PASSWORD"] = "spithas3116"
        os.environ['MAIL_APIKEY_PUBLIC']='...'
        os.environ['MAIL_APIKEY_PRIVATE']='...'

if EXECUTION_ENVIRONMENT=='pythonanywhere':
    os.environ["RECAPTCHA_SITE_KEY"] = "6LeQxnwUAAAAAAyscnSdBS0RbNo6BEDje-trtOV-"
    os.environ["RECAPTCHA_SECRET_KEY"] = "6LeQxnwUAAAAAGjxVdpUGhRREi5xQQQhRfROJCmZ"
    os.environ["RECAPTCHA_INVISIBLE_SITE_KEY"] = "...."
    os.environ["RECAPTCHA_INVISIBLE_SECRET_KEY"] = "..."
else:
    os.environ["RECAPTCHA_SITE_KEY"] = "6LcD3XkUAAAAABAoO2p4WOoBGg6uRyCoVCcGNCFV"
    os.environ["RECAPTCHA_SECRET_KEY"] = "6LcD3XkUAAAAAHTNpV8RsDN8CybCNEJ0htRddCMq"
    os.environ["RECAPTCHA_INVISIBLE_SITE_KEY"] = "6LfL2HkUAAAAAF8ot-2aPAHYzHPAAxvLtKI-PyXi"
    os.environ["RECAPTCHA_INVISIBLE_SECRET_KEY"] = "6LfL2HkUAAAAAIdjgyCwgSaV2hvOS6APpoXot1yw"

################################################################
### Secret key for signing cookies
################################################################
SECRET_KEY = os.environ.get('SECRET_KEY') or '....'
SECURITY_PASSWORD_SALT = '...'
################################################################
### database config
################################################################
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = True
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimides_db'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db'
print('###instance### ###config.py### SQLALCHEMY_DATABASE_URI=',SQLALCHEMY_DATABASE_URI)
username = "ganimides"
password = "philea13"
hostname = "ganimides.mysql.pythonanywhere-services.com"
databasename = "ganimides$ganimides_db"
database_username = "ganimides"
database_password = "spithas13"
SQLALCHEMY_DATABASE_URI2 = "mysql+{mysqlconnector}://{username}:{password}@{hostname}/{databasename}".format(
    mysqlconnector="pymysql",
    username="ganimides",
    password="philea13",
    hostname="ganimides.mysql.pythonanywhere-services.com",
    databasename="ganimides$ganimides_db"
)
print('###instance### ###config.py### SQLALCHEMY_DATABASE_URI2=',SQLALCHEMY_DATABASE_URI)
#db = SQLAlchemy(app, engine = create_engine("mysql+myqldb://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db", pool_recycle=280))
#mysql://InsulT:password@mysql.server/InsulT$default'
#{
#    "host": "localhost",
#    "user": "root",
#    "password": "philea13",
#    "database": "db",
#    "sql_engine": "mysql+pymysql",
#    "charset": "utf8"
#}
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
#DATABASE_CONNECT_OPTIONS = {}
#############################################################################################
# mail server
#############################################################################################
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in ['true', 'on', '1']
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '...@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '****')
MAIL_APIKEY_PUBLIC = os.environ['MAIL_APIKEY_PUBLIC']
MAIL_APIKEY_PRIVATE = os.environ['MAIL_APIKEY_PRIVATE']

## mail settings google
#MAIL_SERVER = 'smtp.googlemail.com'
#MAIL_PORT = 465
#MAIL_USE_TLS = False
#MAIL_USE_SSL = True
#MAIL_USERNAME = "ganimidis@gmail.com"
#MAIL_PASSWORD = "philea13"

## mail settings yandex
#MAIL_SERVER = 'smtp.yandex.ru'
#MAIL_PORT = 587
#MAIL_USE_TLS = True
#MAIL_USE_SSL = True
#MAIL_USERNAME = 'ganimides' # only login without @yandex.ru
#MAIL_PASSWORD = '******'
#############################################################################################
### mail accounts
#############################################################################################
MAIL_SENDER = 'noreply@ganimides.com>'
MAIL_SUBJECT_PREFIX = '[ganimides]'
MAIL_DEFAULT_SENDER = 'noreply@ganimides.com'
MAIL_ADMIN_SENDER = 'admin@ganimides.com'
MAIL_SUPPORT_SENDER = 'support@ganimides.com'
WEBSITE_ADMIN = os.environ.get('WEBSITE_ADMIN')
#############################################################################################
#google recapcha
#############################################################################################
RECAPTCHA_SITE_KEY=os.environ["RECAPTCHA_SITE_KEY"]
RECAPTCHA_SECRET_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
RECAPTCHA_INVISIBLE_SITE_KEY=os.environ["RECAPTCHA_INVISIBLE_SITE_KEY"]
RECAPTCHA_INVISIBLE_SECRET_KEY=os.environ["RECAPTCHA_INVISIBLE_SECRET_KEY"]
RECAPTCHA_PUBLIC_KEY=os.environ["RECAPTCHA_SITE_KEY"]
RECAPTCHA_PRIVATE_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
GOOGLE_RECAPTCHA_CHECKBOX_SITE_KEY=os.environ["RECAPTCHA_SITE_KEY"]
GOOGLE_RECAPTCHA_CHECKBOX_SECRET_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY=os.environ["RECAPTCHA_SITE_KEY"]
GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
################################################################
### miscellaneous
################################################################
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SSL_REDIRECT = False
# Application threads. A common general assumption is using 2 per available processor cores - to handle incoming requests using one and performing background operations using the other.
THREADS_PER_PAGE = 2
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True
# Use a secure, unique and absolutely secret key for signing the data.
CSRF_SESSION_KEY = "aeiotheosomegasgeometrei"
################################################################

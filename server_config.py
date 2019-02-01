# myServer/server_config.py
import os
# # #3 #4 #5
print(__file__)
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#filename = os.path.basename(__file__)
filename = __file__.replace(BASE_DIR, '').replace('\\..', '').replace('\\', '')
print(filename)

EYECATCH = 'SERVER'
SERVER = 'localhost'
BASE_DIR = basedir
EXECUTION_MODE = 'development'

EXECUTION_ENVIRONMENT = 'pythonanywhere'
EXECUTION_ENVIRONMENT = 'localhost'
MAIL_SERVER_PROVIDER = 'google' #'mailjet' #'yandex'

################################################################
### mail servers
################################################################
mailjet_MAIL_SERVER = 'in-v3.mailjet.com'
mailjet_MAIL_PORT = '587' #Port 25 or 587 (some providers block port 25). If TLS on port 587 doesn't work, try using port 465 and/or using SSL instead
mailjet_MAIL_USE_TLS = 'True'
mailjet_MAIL_USE_SSL = 'True'
mailjet_MAIL_USERNAME = 'f8d33207c3c7a1ecaf2f74e809b57786'
mailjet_MAIL_PASSWORD = '2d6a3c2de41ff45b5435382f3e267580'
mailjet_MAIL_APIKEY_PUBLIC ='f8d33207c3c7a1ecaf2f74e809b57786'
mailjet_MAIL_APIKEY_PRIVATE ='2d6a3c2de41ff45b5435382f3e267580'

yandex_MAIL_SERVER = "smtp.yandex.ru"
yandex_MAIL_PORT = '587'
yandex_MAIL_USE_TLS = 'True'
yandex_MAIL_USE_SSL = 'True'
yandex_MAIL_USERNAME = '...' #without the @yandex.ru
yandex_MAIL_PASSWORD = '***'
yandex_MAIL_APIKEY_PUBLIC ='...'
yandex_MAIL_APIKEY_PRIVATE ='...'

google_MAIL_SERVER = "smtp.gmail.com"
google_MAIL_PORT = '587'
google_MAIL_USE_TLS = 'False'
google_MAIL_USE_SSL = 'True'
google_MAIL_USERNAME = 'akamas2020@gmail.com'
google_MAIL_PASSWORD = 'philea13'
google_MAIL_USERNAME = 'bstarr131@gmail.com'
google_MAIL_PASSWORD = 'bstarr13'
google_MAIL_USERNAME = 'spithas@leandrou.com'
google_MAIL_PASSWORD = 'spithas3116'
google_MAIL_APIKEY_PUBLIC ='...'
google_MAIL_APIKEY_PRIVATE ='...'

if MAIL_SERVER_PROVIDER == 'mailjet':
    MAIL_SERVER = mailjet_MAIL_SERVER
    MAIL_PORT = mailjet_MAIL_PORT
    MAIL_USE_TLS = mailjet_MAIL_USE_TLS
    MAIL_USE_SSL = mailjet_MAIL_USE_SSL
    MAIL_USERNAME = mailjet_MAIL_USERNAME
    MAIL_PASSWORD = mailjet_MAIL_PASSWORD
    MAIL_APIKEY_PUBLIC = mailjet_MAIL_APIKEY_PUBLIC
    MAIL_APIKEY_PRIVATE = mailjet_MAIL_APIKEY_PRIVATE
else:
    if MAIL_SERVER_PROVIDER =='yandex':
        MAIL_SERVER = yandex_MAIL_SERVER
        MAIL_PORT = yandex_MAIL_PORT
        MAIL_USE_TLS = yandex_MAIL_USE_TLS
        MAIL_USE_SSL = yandex_MAIL_USE_SSL
        MAIL_USERNAME = yandex_MAIL_USERNAME
        MAIL_PASSWORD = yandex_MAIL_PASSWORD
        MAIL_APIKEY_PUBLIC = yandex_MAIL_APIKEY_PUBLIC
        MAIL_APIKEY_PRIVATE = yandex_MAIL_APIKEY_PRIVATE
    else:
        MAIL_SERVER = google_MAIL_SERVER
        MAIL_PORT = google_MAIL_PORT
        MAIL_USE_TLS = google_MAIL_USE_TLS
        MAIL_USE_SSL = google_MAIL_USE_SSL
        MAIL_USERNAME = google_MAIL_USERNAME
        MAIL_PASSWORD = google_MAIL_PASSWORD
        MAIL_APIKEY_PUBLIC = google_MAIL_APIKEY_PUBLIC
        MAIL_APIKEY_PRIVATE = google_MAIL_APIKEY_PRIVATE

################################################################
### database connection
################################################################
DATABASE_SERVER = 'localhost'
DATABASE_NAME = 'ifestionas_db'
DATABASE_SERVER_URI = 'mysql+pymysql://ganimedes:philea13@localhost'
DATABASE_URI = DATABASE_SERVER_URI+'/'+DATABASE_NAME

localhost_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimedes_db'
pythonanywhere_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ifestionas:philea13@ifestionas.mysql.pythonanywhere-services.com/ifestionas$ganimides_db'
pythonanywhere_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db'
localhost_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ifestionas_db'
localhost_SQLALCHEMY_TEST_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimedes_db_test'

SQLALCHEMY_DATABASE_URI = localhost_SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TEST_DATABASE_URI = localhost_SQLALCHEMY_TEST_DATABASE_URI
SQLALCHEMY_DATABASE_URI = localhost_SQLALCHEMY_DATABASE_URI
if EXECUTION_ENVIRONMENT == 'pythonanywhere':
    DATABASE_SERVER = 'ganimides.mysql.pythonanywhere-services.com'
    DATABASE_NAME = 'ganimides$ganimides_db'
    DATABASE_SERVER_URI = 'mysql+pymysql://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com'
    DATABASE_URI = DATABASE_SERVER_URI+'/'+DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = pythonanywhere_SQLALCHEMY_DATABASE_URI

# #SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimedes_db'
# #{
# #    "host": "localhost",
# #    "user": "root",
# #    "password": "philea13",
# #    "database": "db",
# #    "sql_engine": "mysql+pymysql",
# #    "charset": "utf8"
# #}
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimides_db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db'
# #print('      ', filename, __name__, '###instance### ###config.py### SQLALCHEMY_DATABASE_URI=',SQLALCHEMY_DATABASE_URI)
# username = "ganimides"
# password = "philea13"
# hostname = "ganimides.mysql.pythonanywhere-services.com"
# databasename = "ganimides$ganimides_db"
# database_username = "ganimides"
# database_password = "spithas13"
# SQLALCHEMY_DATABASE_URI2 = "mysql+{mysqlconnector}://{username}:{password}@{hostname}/{databasename}".format(
#     mysqlconnector="pymysql",
#     username="ganimides",
#     password="philea13",
#     hostname="ganimides.mysql.pythonanywhere-services.com",
#     databasename="ganimides$ganimides_db"
# )
# #db = SQLAlchemy(app, engine = create_engine("mysql+myqldb://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db", pool_recycle=280))
# #mysql://InsulT:password@mysql.server/InsulT$default'
# #{
# #    "host": "localhost",
# #    "user": "root",
# #    "password": "philea13",
# #    "database": "db",
# #    "sql_engine": "mysql+pymysql",
# #    "charset": "utf8"
# #}
# #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
# #DATABASE_CONNECT_OPTIONS = {}



################################################################
### recaptcha config
################################################################
localhost_google_RECAPTCHA_SITE_KEY = "6LcD3XkUAAAAABAoO2p4WOoBGg6uRyCoVCcGNCFV"
localhost_google_RECAPTCHA_SECRET_KEY = "6LcD3XkUAAAAAHTNpV8RsDN8CybCNEJ0htRddCMq"
localhost_google_RECAPTCHA_INVISIBLE_SITE_KEY = "6LfL2HkUAAAAAF8ot-2aPAHYzHPAAxvLtKI-PyXi"
localhost_google_RECAPTCHA_INVISIBLE_SECRET_KEY = "6LfL2HkUAAAAAIdjgyCwgSaV2hvOS6APpoXot1yw"

pythonanywhere_google_RECAPTCHA_SITE_KEY = "6LeQxnwUAAAAAAyscnSdBS0RbNo6BEDje-trtOV-"
pythonanywhere_google_RECAPTCHA_SECRET_KEY = "6LeQxnwUAAAAAGjxVdpUGhRREi5xQQQhRfROJCmZ"
pythonanywhere_google_RECAPTCHA_INVISIBLE_SITE_KEY = "...."
pythonanywhere_google_RECAPTCHA_INVISIBLE_SECRET_KEY = "..."

RECAPTCHA_SITE_KEY = localhost_google_RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY = localhost_google_RECAPTCHA_SECRET_KEY
RECAPTCHA_INVISIBLE_SITE_KEY = localhost_google_RECAPTCHA_INVISIBLE_SITE_KEY
RECAPTCHA_INVISIBLE_SECRET_KEY = localhost_google_RECAPTCHA_INVISIBLE_SECRET_KEY
GOOGLE_RECAPTCHA_SITE_KEY = localhost_google_RECAPTCHA_SITE_KEY
GOOGLE_RECAPTCHA_SECRET_KEY = localhost_google_RECAPTCHA_SECRET_KEY
GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY = localhost_google_RECAPTCHA_INVISIBLE_SITE_KEY
GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY = localhost_google_RECAPTCHA_INVISIBLE_SECRET_KEY
if EXECUTION_ENVIRONMENT=='pythonanywhere':
    RECAPTCHA_SITE_KEY = pythonanywhere_google_RECAPTCHA_SITE_KEY
    RECAPTCHA_SECRET_KEY = pythonanywhere_google_RECAPTCHA_SECRET_KEY
    RECAPTCHA_INVISIBLE_SITE_KEY = pythonanywhere_google_RECAPTCHA_INVISIBLE_SITE_KEY
    RECAPTCHA_INVISIBLE_SECRET_KEY = pythonanywhere_google_RECAPTCHA_INVISIBLE_SECRET_KEY
    GOOGLE_RECAPTCHA_SITE_KEY = pythonanywhere_google_RECAPTCHA_SITE_KEY
    GOOGLE_RECAPTCHA_SECRET_KEY = pythonanywhere_google_RECAPTCHA_SECRET_KEY
    GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY = pythonanywhere_google_RECAPTCHA_INVISIBLE_SITE_KEY
    GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY = pythonanywhere_google_RECAPTCHA_INVISIBLE_SECRET_KEY

RECAPTCHA_PUBLIC_KEY = RECAPTCHA_SITE_KEY
RECAPTCHA_PRIVATE_KEY = RECAPTCHA_SECRET_KEY
RECAPTCHA_INVISIBLE_PUBLIC_KEY = RECAPTCHA_INVISIBLE_SITE_KEY
RECAPTCHA_INVISIBLE_PRIVATE_KEY = RECAPTCHA_INVISIBLE_SECRET_KEY
################################################################
### Secret key for signing cookies
################################################################
SECRET_KEY = 'server-aeiotheosomegasgeometreip9Bv<3Eid9%$i01bobbistarr'
SECURITY_PASSWORD_SALT = 'server-aeiotheosomegasgeometreip9Bvtispaolasbobbistarr'

################################################################
#store in os.environ in order to be used in instance or app_config
################################################################
os.environ["SERVER"]=SERVER
os.environ["EXECUTION_ENVIRONMENT"]=EXECUTION_ENVIRONMENT
os.environ["MAIL_SERVER_PROVIDER"]=MAIL_SERVER_PROVIDER

os.environ["mailjet_MAIL_SERVER"]=mailjet_MAIL_SERVER
os.environ["mailjet_MAIL_PORT"]=mailjet_MAIL_PORT
os.environ["mailjet_MAIL_USE_TLS"]=mailjet_MAIL_USE_TLS
os.environ["mailjet_MAIL_USE_SSL"]=mailjet_MAIL_USE_SSL
os.environ["mailjet_MAIL_USERNAME"]=mailjet_MAIL_USERNAME
os.environ["mailjet_MAIL_PASSWORD"]=mailjet_MAIL_PASSWORD
os.environ["mailjet_MAIL_APIKEY_PUBLIC"]=mailjet_MAIL_APIKEY_PUBLIC
os.environ["mailjet_MAIL_APIKEY_PRIVATE"]=mailjet_MAIL_APIKEY_PRIVATE

os.environ["yandex_MAIL_SERVER"]=yandex_MAIL_SERVER
os.environ["yandex_MAIL_PORT"]=yandex_MAIL_PORT
os.environ["yandex_MAIL_USE_TLS"]=yandex_MAIL_USE_TLS
os.environ["yandex_MAIL_USE_SSL"]=yandex_MAIL_USE_SSL
os.environ["yandex_MAIL_USERNAME"]=yandex_MAIL_USERNAME
os.environ["yandex_MAIL_PASSWORD"]=yandex_MAIL_PASSWORD
os.environ["yandex_MAIL_APIKEY_PUBLIC"]=yandex_MAIL_APIKEY_PUBLIC
os.environ["yandex_MAIL_APIKEY_PRIVATE"]=yandex_MAIL_APIKEY_PRIVATE

os.environ["google_MAIL_SERVER"]=google_MAIL_SERVER
os.environ["google_MAIL_PORT"]=google_MAIL_PORT
os.environ["google_MAIL_USE_TLS"]=google_MAIL_USE_TLS
os.environ["google_MAIL_USE_SSL"]=google_MAIL_USE_SSL
os.environ["google_MAIL_USERNAME"]=google_MAIL_USERNAME
os.environ["google_MAIL_PASSWORD"]=google_MAIL_PASSWORD
os.environ["google_MAIL_APIKEY_PUBLIC"]=google_MAIL_APIKEY_PUBLIC
os.environ["google_MAIL_APIKEY_PRIVATE"]=google_MAIL_APIKEY_PRIVATE

os.environ["MAIL_SERVER"]=MAIL_SERVER
os.environ["MAIL_PORT"]=MAIL_PORT
os.environ["MAIL_USE_TLS"]=MAIL_USE_TLS
os.environ["MAIL_USE_SSL"]=MAIL_USE_SSL
os.environ["MAIL_USERNAME"]=MAIL_USERNAME
os.environ["MAIL_PASSWORD"]=MAIL_PASSWORD
os.environ["MAIL_APIKEY_PUBLIC"]=MAIL_APIKEY_PUBLIC
os.environ["MAIL_APIKEY_PRIVATE"]=MAIL_APIKEY_PRIVATE

os.environ["localhost_SQLALCHEMY_DATABASE_URI"]=localhost_SQLALCHEMY_DATABASE_URI
os.environ["pythonanywhere_SQLALCHEMY_DATABASE_URI"]=pythonanywhere_SQLALCHEMY_DATABASE_URI
os.environ["SQLALCHEMY_DATABASE_URI"]=SQLALCHEMY_DATABASE_URI

os.environ["localhost_google_RECAPTCHA_SITE_KEY"]=localhost_google_RECAPTCHA_SITE_KEY
os.environ["localhost_google_RECAPTCHA_SECRET_KEY"]=localhost_google_RECAPTCHA_SECRET_KEY
os.environ["localhost_google_RECAPTCHA_INVISIBLE_SITE_KEY"]=localhost_google_RECAPTCHA_INVISIBLE_SITE_KEY
os.environ["localhost_google_RECAPTCHA_INVISIBLE_SECRET_KEY"]=localhost_google_RECAPTCHA_INVISIBLE_SECRET_KEY

os.environ["pythonanywhere_google_RECAPTCHA_SITE_KEY"]=pythonanywhere_google_RECAPTCHA_SITE_KEY
os.environ["pythonanywhere_google_RECAPTCHA_SECRET_KEY"]=pythonanywhere_google_RECAPTCHA_SECRET_KEY
os.environ["pythonanywhere_google_RECAPTCHA_INVISIBLE_SITE_KEY"]=pythonanywhere_google_RECAPTCHA_INVISIBLE_SITE_KEY
os.environ["pythonanywhere_google_RECAPTCHA_INVISIBLE_SECRET_KEY"]=pythonanywhere_google_RECAPTCHA_INVISIBLE_SECRET_KEY

os.environ["RECAPTCHA_SITE_KEY"]=RECAPTCHA_SITE_KEY
os.environ["RECAPTCHA_SECRET_KEY"]=RECAPTCHA_SECRET_KEY
os.environ["RECAPTCHA_INVISIBLE_SITE_KEY"]=RECAPTCHA_INVISIBLE_SITE_KEY
os.environ["RECAPTCHA_INVISIBLE_SECRET_KEY"]=RECAPTCHA_INVISIBLE_SECRET_KEY


# ################################################################
# ### print
# ################################################################
print('      ', filename, __name__, EYECATCH, '### BASE_DIR =', BASE_DIR)
print('      ', filename, __name__, EYECATCH, '### SERVER =', SERVER)
print('      ', filename, __name__, EYECATCH, '### EXECUTION_ENVIRONMENT =', EXECUTION_ENVIRONMENT)
print('      ', filename, __name__, EYECATCH, '### EXECUTION_MODE =', EXECUTION_MODE)
print('      ', filename, __name__, EYECATCH, '--------------------------------------------------')
print('      ', filename, __name__, EYECATCH, '### SQLALCHEMY_DATABASE_URI =',SQLALCHEMY_DATABASE_URI)
print('      ', filename, __name__, EYECATCH, '--------------------------------------------------')
print('      ', filename, __name__, EYECATCH, '### MAIL_SERVER_PROVIDER =',MAIL_SERVER_PROVIDER)
print('      ', filename, __name__, EYECATCH, '### MAIL_SERVER =',MAIL_SERVER)
print('      ', filename, __name__, EYECATCH, '### MAIL_PORT =',MAIL_PORT)
print('      ', filename, __name__, EYECATCH, '### MAIL_USE_TLS =',MAIL_USE_TLS)
print('      ', filename, __name__, EYECATCH, '### MAIL_USE_SSL =',MAIL_USE_SSL)
print('      ', filename, __name__, EYECATCH, '### MAIL_USERNAME =',MAIL_USERNAME)
print('      ', filename, __name__, EYECATCH, '### MAIL_PASSWORD =',MAIL_PASSWORD)
print('      ', filename, __name__, EYECATCH, '### MAIL_APIKEY_PUBLIC =',MAIL_APIKEY_PUBLIC)
print('      ', filename, __name__, EYECATCH, '### MAIL_APIKEY_PRIVATE =',MAIL_APIKEY_PRIVATE)
print('      ', filename, __name__, EYECATCH, '--------------------------------------------------')
print('      ', filename, __name__, EYECATCH, '### GOOGLE_RECAPTCHA_SITE_KEY =',GOOGLE_RECAPTCHA_SITE_KEY)
print('      ', filename, __name__, EYECATCH, '### GOOGLE_RECAPTCHA_SECRET_KEY =',GOOGLE_RECAPTCHA_SECRET_KEY)
print('      ', filename, __name__, EYECATCH, '### GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY =',GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY)
print('      ', filename, __name__, EYECATCH, '### GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY =',GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY)
print('      ', filename, __name__, EYECATCH, '--------------------------------------------------')
print('      ', filename, __name__, EYECATCH, '### SECRET_KEY =',SECRET_KEY)
print('      ', filename, __name__, EYECATCH, '### SECURITY_PASSWORD_SALT =',SECURITY_PASSWORD_SALT)
print('      ', filename, __name__, EYECATCH, '--------------------------------------------------')
#############################################################################################

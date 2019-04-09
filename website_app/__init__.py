# myApp/__init__.py
"""
The flask application package.
"""
import os
import os.path
from os import environ
import configparser

import sqlalchemy
from datetime import datetime
# third-party imports
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# local imports
from .config import app_config, environment_config, execmode_config
from website_app.debug_services.debug_log_services import *
from .config_debug import debug_config_startup, debug_config_execution

#from logging.config import dictConfig
#from .external_services.log_services import *
#log_info('###dictConfig###', dictConfig)

#################logging#######
#logging config
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
#logger.setLevel(logging.INFO)

# create a file handler
# handler = logging.FileHandler('hello.log')
# handler.setLevel(logging.DEBUG)

# # create a logging format
# formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
# handler.setFormatter(formatter)

# # add the handlers to the logger
# logger.addHandler(handler)

# test the logger
logger.info('#################################################Hello World################################')

# CRITICAL	50
# ERROR	40
# WARNING	30
# INFO	20
# DEBUG	10
# NOTSET	0

logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.basicConfig(level=logging.ERROR)
#logging.Formatter('%(asctime)s | %(name)s | %(levelname)s |:: %(message)s ::')
# def create_app():
#     app = Flask(__name__)
#     db.init_app(app)
#     return app

################################################################################
debug_config_startup()
################################################################################


################################################################################
log_init_start(__file__,'app_init')
################################################################################

### Define the database
db = SQLAlchemy()
log_info('db = SQLAlchemy()')
# db variable initialization
#db = SQLAlchemy(session_options={"expire_on_commit": False, "pool_pre_ping": True})
#sqlalchemy.pool_recycle = 3600
#print('####################db.pool_recycle########',db.pool_recycle)
#db.pool_recycle = 90
#print('####################db.pool_recycle########',db.pool_recycle)
#db = SQLAlchemy(session_options={"expire_on_commit": False})
#pool_size, max_overflow, pool_recycle
#db.pool_recycle = 90

################################################################################
################################################################################
################################################################################
### configuaration folders and files
################################################################################
################################################################################
################################################################################
thisfile = os.path.abspath(__file__)
thisDir = os.path.dirname(__file__)
thisFileName = os.path.basename(__file__)
thisFolderName = os.path.basename(thisDir)
exec_folder = os.path.abspath(os.path.dirname(__file__))
app_config_folder = os.path.dirname(exec_folder)
app_ini_filename = 'app.ini'
#app_config_filename = 'app_config.py'
app_ini_file = os.path.join(app_config_folder, app_ini_filename)
#app_config_file = os.path.join(app_config_folder, app_config_filename)
app_relative_config_path = '..\{}'.format(thisFolderName)
app_relative_config_path = ''
################################################################
# print('...App_Startup_Program =', __file__)
# print('...App_Startup_Folder =', thisDir)
# print('...App_Startup_FolderName =', thisFolderName)
# print('...App_Startup_ProgramName =', thisFileName)
# print('...App_Exec_Folder =', exec_folder)
# print('...App_Config_Folder =', app_config_folder)
# print('...App_ini_file =', app_ini_file)
# print('...App_config_file =', app_config_file)
# print('...App_ini_file_name =', app_ini_filename)
# print('...App_config_file_name =', app_config_filename)
# print('...app_relative_config_path = app_relative_config_path
#print (os.path.isfile(app_config_file))
################################################################
AppDictionary = {}
AppDictionary.update({'app_Startup_Program':__file__})
AppDictionary.update({'app_Startup_Folder':thisDir})
AppDictionary.update({'app_Startup_Folder_Name':thisFolderName})
AppDictionary.update({'app_Startup_Program_Name':thisFileName})
AppDictionary.update({'app_Startup_Execfolder':exec_folder})
AppDictionary.update({'app_Config_Folder':app_config_folder})
AppDictionary.update({'app_ini_file_Name':app_ini_filename})
#AppDictionary.update({'app_config_file_Name':app_config_filename})
AppDictionary.update({'app_ini_file':app_ini_file})
#AppDictionary.update({'app_config_file':app_config_filename})
AppDictionary.update({'app_relative_config_path':app_relative_config_path})
for appitem in AppDictionary:
    os.environ[appitem.upper()] = AppDictionary.get(appitem)
    log_env_param(appitem.upper(), os.environ.get(appitem.upper()))
################################################################
app_relative_config_path = os.environ.get('APP_RELATIVE_CONFIG_PATH')
server_relative_config_path = os.environ.get('SERVER_RELATIVE_CONFIG_PATH')
app_Startup_Folder = os.environ.get('APP_STARTUP_FOLDER')
log_warning('app_Startup_Folder', app_Startup_Folder)
log_warning('app_relative_config_path', app_relative_config_path)
log_warning('server_relative_config_path', server_relative_config_path)
################################################################
#for debug: list all env params
# for envitem in os.environ:
#     print('...env param: '+envitem+' =', os.environ.get(envitem))


#exit(0)


################################################################################
################################################################################
################################################################################
### Define the WSGI application object
################################################################################
################################################################################
################################################################################
log_info('###CREATE FLASK-APP###', 'app = Flask(__name__, instance_relative_config=True)')
#app = Flask(__name__, instance_relative_config=True)
app = Flask(__name__, instance_path=app_Startup_Folder)
#x=get_instance_folder_path()
#log_variable('get_instance_folder_path', x)
log_variable('app', app)
log_file('app.instance_path', app.instance_path)
log_file('app.template_folder', app.template_folder)
log_file('app.static_folder', app.static_folder)
#exit(0)
#--> important: the folders are relative to where the flask app is created
# specifies the main template folder for the application
#app = Flask(__name__,
#            instance_path=get_instance_folder_path(),
#            instance_relative_config=True,
#            template_folder='templates')
#log_info('###SQLALCHEMY_POOL_RECYCLE####', app.config['SQLALCHEMY_POOL_RECYCLE'])

# ################################################################
# #server config
# ################################################################
# move server configuration from os.env to app.config
config_name = 'server'
arrEnvServerKeys = os.environ.get('SERVER_INI_KEYS').split(sep=',')
#print("arrEnvServerKeys =",arrEnvServerKeys)
for ix, key in enumerate(arrEnvServerKeys):
    app.config[key] = os.environ.get(key)
    #print(ix, 'app key from env key', key, '=', app.config.get(key))
    msg = '{}. app key from env key {}={}'.format(ix, key, app.config.get(key))
    log_config_param(key, app.config.get(key))
log_info('CONFIG-STEP-1 SERVER_CONFIGURATION', ix, ' env keys added to app.config')

################################################################
#app.ini
################################################################
for appitem in AppDictionary:
    app.config[appitem.upper()] = AppDictionary.get(appitem)

if app_ini_file and os.path.isfile(app_ini_file):
    if os.access(app_ini_file, os.R_OK):
        log_info('app_ini_file FOUND...', app_ini_file)
        #log_start('app.ini')
        #os.environ["app_ini_file"] = app_ini_file
        config = configparser.ConfigParser()
        config.read(app_ini_file)
        i=0
        for section in config:
            i = i + 1
            k = 0
            log_info('app.ini section =', section)
            for key in config[section]:
                k = k + 1
                #os.environ[key.upper()] = config[section][key].replace("'", "")
                app.config[key.upper()] = config[section][key].replace("'", "")
                log_config_param(key.upper(), config[section][key])
        #log_finish('app.ini')
    else:
        log_warning('app.ini file [', app_ini_file, '] the file is not readable')
else:
    log_warning('app.ini file NOT-FOUND:[', app_ini_file, ']')
log_info('CONFIG-STEP-2 APPLICATION_CONFIGURATION from APP.INI')

### app flask config
################################################################################
################################################################################
################################################################################
### Configurations
################################################################################
################################################################################
################################################################################
#log_info('')
log_info('###CONFIGURE FLASK-APP###')
################################################################################
################################################################################



################################################################################
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
log_info('FLASK_CONFIGURATION', config_name)
#exit(0)
# enable jinja2 extensions - i.e. continue in for loops
#app.jinja_env.add_extension('jinja2.ext.loopcontrols')
#...

#########################################################################################
config_name = 'flask'
#log_info('CONFIG-STEP-1 FLASK_CONFIGURATION', config_name, 'from app_config in .config.py')
app.config.from_object(app_config[config_name]) # object-based default configuration
log_info('CONFIG-STEP-3 FLASK_CONFIGURATION', config_name, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

# #########################################################################################
# config_name = 'pagination'
# #log_info('CONFIG-STEP-1 FLASK_CONFIGURATION', config_name, 'from app_config in .config.py')
# app.config.from_object(app_config[config_name]) # object-based default configuration
# log_info('CONFIG-STEP-2 FLASK_CONFIGURATION', config_name, 'EYECATCH---', app.config.get('EYECATCH'))
# print('###PER_PAGE', app.config.get('PER_PAGE'))
    
# #########################################################################################

#... more apps here

#########################################################################################
config_name = 'google'
config_file_name = 'config_google.py'
config_file = '..\website_app\config_google.py'
config_file = 'config_google.py'
config_file = '{}\{}'.format(app_relative_config_path, config_file_name)
app.config.from_pyfile(config_file_name, silent=False) # instance-folders configuration (outside source control)
log_info('CONFIG-STEP-5 google apps', config_file, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#########################################################################################
config_name = 'geolocation'
config_file_name = 'config_geolocation.py'
config_file = '..\website_app\config_geolocation.py'
config_file = '{}\{}'.format(app_relative_config_path, config_file_name)
app.config.from_pyfile(config_file_name, silent=False) # instance-folders configuration (outside source control)
log_info('CONFIG-STEP-6 geolocation', config_file, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#########################################################################################
config_name = 'mailserver'
config_file_name = 'config_mailserver.py'
config_file = '..\website_app\config_mailserver.py'
config_file = '{}\{}'.format(app_relative_config_path, config_file_name)
app.config.from_pyfile(config_file_name, silent=False) # instance-folders configuration (outside source control)
log_info('CONFIG-STEP-7 mailserver', config_file, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#########################################################################################
config_name = app.config.get('EXECUTION_ENVIRONMENT')
if os.getenv('EXECUTION_ENVIRONMENT', ''):
    config_name = os.getenv('EXECUTION_ENVIRONMENT')
if not config_name:
    config_name = 'localhost'
app.config.from_object(environment_config[config_name]) # object-based default configuration
log_info('CONFIG-STEP-8 EXECUTION_ENVIRONMENT', config_name, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#########################################################################################
config_name = app.config.get('EXECUTION_MODE')
if os.getenv('EXECUTION_MODE', ''):
    config_name = os.getenv('EXECUTION_MODE')
if not config_name:
    config_name = 'design'
app.config.from_object(execmode_config[config_name]) # object-based default configuration
log_info('CONFIG-STEP-9 EXECUTION_MODE', config_name, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#########################################################################################
config_name = 'database'
config_file_name = 'config_database.py'
config_file = '..\website_app\config_database.py'
config_file = '{}\{}'.format(app_relative_config_path, config_file_name)
app.config.from_pyfile(config_file_name, silent=False) # instance-folders configuration (outside source control)
log_info('CONFIG-STEP-10 database', config_file, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#########################################################################################
config_name = 'sqlalchemy'
config_file_name = 'config_sqlalchemy.py'
config_file = '..\config_sqlalchemy.py'
config_file = '..\website_app\config_database.py'
config_file = '{}\{}'.format(app_relative_config_path, config_file_name)
app.config.from_pyfile(config_file_name, silent=False) # instance-folders configuration (outside source control)
log_info('CONFIG-STEP-11 database', config_file, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#########################################################################################
config_name = 'pagination'
config_file_name = 'config_pagination.py'
config_file = '{}\{}'.format(app_relative_config_path, config_file_name)
app.config.from_pyfile(config_file_name, silent=False) # instance-folders configuration (outside source control)
log_info('CONFIG-STEP-12', config_name, config_file, 'EYECATCH---', app.config.get('EYECATCH'))
#########################################################################################

#log_start('config_checkpoint_1')
log_checkpoint('1', 'EXECUTION_MODE---', app.config['EXECUTION_MODE'])
log_checkpoint('1', 'SERVER---', app.config['SERVER'])
log_checkpoint('1', 'DATABASE_SERVER---', app.config['DATABASE_SERVER'])
log_checkpoint('1', 'DATABASE_NAME---', app.config['DATABASE_NAME'])
log_checkpoint('1', 'DATABASE_SERVER_URI---', app.config['DATABASE_SERVER_URI'])
log_checkpoint('1', 'DATABASE_URI---', app.config['DATABASE_URI'])
log_checkpoint('1', 'SQLALCHEMY_DATABASE_URI---', app.config['SQLALCHEMY_DATABASE_URI'])
log_checkpoint('1', 'RECAPTCHA_PUBLIC_KEY---', app.config['RECAPTCHA_PUBLIC_KEY'])
log_checkpoint('1', 'RECAPTCHA_PRIVATE_KEY---', app.config['RECAPTCHA_PRIVATE_KEY'])
#log_finish('config_checkpoint_1')

################################################################################
################################################################################
################################################################################
### app variables
################################################################################
################################################################################
################################################################################
#required for splash forms: will be set in @app.before_first_request
log_info('###APP VARIABLES###')
app.loginform = None
app.registrationform = None
app.contactusform = None
app.forgetpasswordform = None
app.cookiesconsentform = None
app.splashform = None
app.homepage_html = 'page_templates/landing_page.html'
app.modules_stack = []
app.modules_stack.append(__name__)
##-##-####-##-####-##-####-##-####-##-##
#log_info('Start')
##-##-####-##-####-##-####-##-####-##-##
################################################################################
################################################################################
################################################################################
#log_start('config_checkpoint_2')
log_checkpoint('2', 'app.homepage_html---', app.homepage_html)
log_checkpoint('2', 'SPLASH FORM---', app.config['SPLASHFORM_LOGIN'])
log_checkpoint('2', 'SPLASH FORM---', app.config['SPLASHFORM_REGISTRATION'])
log_checkpoint('2', 'SPLASH FORM---', app.config['SPLASHFORM_FORGETPASSWORD'])
log_checkpoint('2', 'SPLASH FORM---', app.config['SPLASHFORM_CONTACTUS'])
#log_finish('config_checkpoint_2')
################################################################################
################################################################################
################################################################################
### ?????????????
################################################################################
################################################################################
################################################################################
#log_info('')
log_info('###BOOTSTRAP APP###', 'Bootstrap(app)')
Bootstrap(app)
#####################################################################
################################################################################
################################################################################
### Define the database object which is imported by modules and controllers
################################################################################
################################################################################
################################################################################
log_info('###DATABASE###','define database:db = SQLAlchemy(app)')
#db = SQLAlchemy(session_options={"expire_on_commit": False, "pool_pre_ping": True})
#db = SQLAlchemy()
db.init_app(app)
################################################################################
################################################################################
################################################################################
## sqlalchemy pool
################################################################################
################################################################################
log_info('###DATABASE###','sqlalchemy.create_engine')
#import sqlalchemy
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select
DATABASE_URI = app.config['DATABASE_URI']
some_engine = sqlalchemy.create_engine(DATABASE_URI, pool_recycle=80)  # connect to database
#e = create_engine("mysql+pymysql://scott:tiger@mysql57/test?charset=utf8mb4&binary_prefix=true", echo=True)

@event.listens_for(some_engine, "engine_connect")
def ping_connection(connection, branch):
    print('###__INIT__###','@@@@ping_connection')
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False

    print('###__INIT__###','@@@@try select 1')
    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
    finally:
        # restore "close with result"
        print('###__INIT__###','@@@@close with result')
        connection.should_close_with_result = save_should_close_with_result


################################################################################
################################################################################
################################################################################
### LoginManager
################################################################################
################################################################################
################################################################################
#log_info('')
log_info('###LOGIN-MANAGER###','login_manager = LoginManager(application)')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "authorization.login"
################################################################################
################################################################################
################################################################################
### Migration Manager
################################################################################
################################################################################
################################################################################
#log_info('')
log_info('###Migration-MANAGER###')
# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)
# #manager.run(db)
#log_finish('###Migration-MANAGER###')
################################################################################
################################################################################
################################################################################
### Home page
################################################################################
################################################################################
################################################################################
#log_info('')
#log_info('###HOME_PAGE###',"render_template('page_templates/landing_page.html',title='landing page')")
#@app.route('/')
#def landingpage():
#    log_info('LANDINGPAGE',request.method,request.url)
#    #session['username'] = "someuser"
#    #session['urls'] = []
#    return render_template('page_templates/landing_page.html',title='landing page'
#    )
################################################################################
################################################################################
################################################################################
### HTTP Error Handlers
################################################################################
################################################################################
################################################################################
#log_info('')
log_info('###ERROR_HANDLERS###')
log_info('@app.errorhandler(403)','render_template(error_pages/403.html, title=Forbidden)')
@app.errorhandler(403)
def forbidden(error):
    print('###__INIT__###','@@@app.errorhandler(403) title=Forbidden)')
    return render_template('error_pages/403.html', title='Forbidden'), 403

log_info('@app.errorhandler(404)','render_template(error_pages/404.html, title=Page Not Found)')
@app.errorhandler(404)
def page_not_found(error):
    print('###__INIT__###','@@@app.errorhandler(404) title=Page Not Found)')
    varPageName = str(request._get_current_object())
    print('###__INIT__###','@@@varPageName', varPageName)
    #return render_template('error_pages/404.html', title='Page Not Found', PageNotFound=varPageName), 404
    return render_template('error_pages/404.html', title='Page Not Found')

log_info('@app.errorhandler(500)','render_template(error_pages/500.html, title=Server Error)')
@app.errorhandler(500)
def internal_server_error(error):
    print('###__INIT__###','@@@app.errorhandler(500) title=Server Error)')
    return render_template('error_pages/500.html', title='Server Error'), 500

#log_finish('###ERROR_HANDLERS###')
################################################################################
################################################################################
################################################################################
# import home pages
################################################################################
################################################################################
################################################################################
log_info('###HOME PAGES###')
from . import views
################################################################################
################################################################################
################################################################################
# Register blueprint(s) for pages
################################################################################
################################################################################
################################################################################
#log_info('')
log_info('###BLUEPRINTS (SUB-APPCOMPONENTS)###')
# Import modules/components using their blueprint handler variable i.e module_authoroization

### authorization module
from . module_authorization.routes import authorization as authorization_module
app.register_blueprint(authorization_module, url_prefix='/authorization')
log_info('authorization_module---', 'app.register_blueprint(authorization_module,url_prefix=''/authorization'')')

### administration module
from . module_administration.routes import administration as administration_module
app.register_blueprint(administration_module, url_prefix='/administration')
log_info('administration_module---', 'app.register_blueprint(administration_module,url_prefix=''/administration'')')

### protototypes page
#from . module_prototypes.controllers import prototypes as prototypes_module
#app.register_blueprint(prototypes_module,url_prefix='/prototypes')
#log_info('prototypes_module---','app.register_blueprint(prototypes_module,url_prefix=''/prototypes'')')

#from app import models
#from .admin import admin as admin_blueprint
#app.register_blueprint(admin_blueprint, url_prefix='/admin')
#log_finish('###BLUEPRINTS (SUB-APPCOMPONENTS)###')
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
# Build the database:This will create the database file using SQLAlchemy
################################################################################
################################################################################
################################################################################
log_info('###DATABASE### create database')
#create the database if not exists
# SERVER = app.config['SERVER'] # application server
# DATABASE_SERVER = app.config['DATABASE_SERVER']
# DATABASE_NAME = app.config['DATABASE_NAME']
# DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
# DATABASE_SERVER_URI = app.config['DATABASE_SERVER_URI']
# DB_URI = app.config['DATABASE_URI']
from database import init_database as init_application_database
from website_app.module_authorization.database import init_database as init_authorization_database
from website_app.module_administration.database import init_database as init_administration_database

log_info('###DATABASE###db.create_all(app=app)')
db.create_all(app=app)
#log_finish('###DATABASE###db.create_all(app=app)')

init_application_database()
init_administration_database()
init_authorization_database()

# dbserver_engine = sqlalchemy.create_engine(DATABASE_SERVER_URI,pool_recycle=180) # connect to server
# existing_databases = dbserver_engine.execute("SHOW DATABASES;")
# existing_databases = [d[0] for d in existing_databases]
# # for database in existing_databases:
# #     print("...database {0} on dbserver {1}".format(database, DATABASE_SERVER_URI))
# if DATABASE_NAME not in existing_databases:
#     dbserver_engine.execute("CREATE DATABASE {db}".format(db=DATABASE_NAME))
#     log_info('###DATABASE###', "{0} database CREATED on DBserver {1}".format(DATABASE_NAME, DATABASE_SERVER))
# else:
#     log_info('###DATABASE###', "database {0} already exists on DBserver {1}".format(DATABASE_NAME, DATABASE_SERVER))
# # -or-
# # dbserver_engine.execute("CREATE DATABASE IF NOT EXISTS {db}".format(db=DATABASE_NAME))
# # dbserver_engine.execute("USE {db}".format(db=DATABASE_NAME))
# dbserver_engine.execute("USE {db}".format(db=DATABASE_NAME))
# dbserver_engine.dispose()

# log_info('###DATABASE###', 'create tables if not exists')
# from .module_administration.models import User, Department, Role
# from .module_authorization.models import Subscriber, ContactMessage
# from .models import Visit, VisitPoint, Page_Visit

# # recreate tables etc
# log_info('###DATABASE###', 'tables created')
# db_engine = sqlalchemy.create_engine(DATABASE_URI, pool_recycle=180) # connect to database
# existing_tables_before = db_engine.execute('SHOW TABLES;')
# existing_tables_before = [d[0] for d in existing_tables_before]
# #print('   ', 'database-init', __name__, 'tables before')
# #list_tables(db_engine)

#log_info('###DATABASE###', 'db.create_all(app=app)')
#db.create_all(app=app)

#db.session.commit()
#print(db.__dir__.__name__)

# existing_tables_after = db_engine.execute('SHOW TABLES;')
# existing_tables_after = [d[0] for d in existing_tables_after]
# created = 0
# for table in existing_tables_after:
#     if table not in existing_tables_before:
#         created = created + 1

# log_info('###DATABASE###',"{0} tables created in database {1}".format(created,DATABASE_NAME))
# db_engine.dispose()
#log_finish('###DATABASE### create database')

################################################################################
################################################################################
################################################################################
## sqlalchemy pool
################################################################################
################################################################################
log_info('###DATABASE###_sqlalchemy.create_engine')
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select
DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
some_engine = sqlalchemy.create_engine(DATABASE_URI, pool_recycle=80) # connect to database

log_info('###DATABASE###','@event.listens_for',"engine_connect",some_engine)
@event.listens_for(some_engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        print('###__INIT__###', 'ping_connection-branch @@@@event.listens_for',"engine_connect",some_engine)
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        print('###__INIT__###', 'ping_connection-try(select([1])) @@@@event.listens_for',"engine_connect")
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        print('###__INIT__###', 'ping_connection-except(select([1])) @@@@event.listens_for',"engine_connect")
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            print('###__INIT__###', 'ping_connection-except-err.connection_invalidated-retry @@@@event.listens_for',"engine_connect")
            connection.scalar(select([1]))
        else:
            print('###__INIT__###', 'ping_connection-except-raise-exception @@@@event.listens_for',"engine_connect")
            raise
    finally:
        # restore "close with result"
        print('###__INIT__###', 'ping_connection-finally:restore close with result @@@@event.listens_for',"engine_connect")
        connection.should_close_with_result = save_should_close_with_result

#log_finish('###DATABASE###_sqlalchemy.create_engine')
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
### functions and variables
################################################################################
################################################################################
################################################################################
#log_info('')
log_info('###FUNCTIONS & VARIABLES###')
def get_time():
    now = datetime.now()
    time=now.strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(name, surname, email):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, Name={}, Surname={}, Email={} \n'.format(timestamp, name, surname, email))
    data.close()
################################################################################
################################################################################
################################################################################
################################################################################
### context processor
################################################################################
################################################################################
################################################################################
#from yourapplication.database import db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        print('###__INIT__###', exception,'@app.teardown_appcontext:','db_session.remove()')
        print('###__INIT__### exception is:', exception)
        #db.db_session.remove()

@app.context_processor
def inject_configuration_parameters_as_variables():
    #log_info('###SERVER_APP_RUNNING###','inject_configuration_parameters_as_variables:')
    #print('   ', '!!! splash forms objects made available by the server...')
    return dict(
        EXECUTION_MODE=app.config['EXECUTION_MODE']
        ,SERVER = app.config['SERVER'] # application server
        ,DATABASE_SERVER = app.config['DATABASE_SERVER']
        ,DATABASE_NAME = app.config['DATABASE_NAME']
        ,DATABASE_URI=app.config['SQLALCHEMY_DATABASE_URI']
        ,DATABASE_SERVER_URI=app.config['DATABASE_SERVER_URI']
        ,DB_URI=app.config['DATABASE_URI']
        ,RECAPTCHA_PUBLIC_KEY=app.config['RECAPTCHA_PUBLIC_KEY']
        ,RECAPTCHA_PRIVATE_KEY=app.config['RECAPTCHA_PRIVATE_KEY']
        ,LAYOUTS_FOLDER=app.config['LAYOUTS_FOLDER']
        ,TEMPLATES_FOLDER=app.config['TEMPLATES_FOLDER']
        ,FORMS_FOLDER=app.config['FORMS_FOLDER']
        ,PAGES_FOLDER=app.config['PAGES_FOLDER']
        ,COMPONENTS_FOLDER=app.config['COMPONENTS_FOLDER']
        ,IMAGES_FOLDER=app.config['IMAGES_FOLDER']
        ,PICTURES_FOLDER=app.config['PICTURES_FOLDER']
        ,UPLOAD_FOLDER=app.config['UPLOAD_FOLDER']
        ,AUTHORIZATION_FOLDER=app.config['AUTHORIZATION_FOLDER']
        ,ALLOWED_EXTENSIONS=app.config['ALLOWED_EXTENSIONS']
        ,AVAILABLE_LANGUAGES=app.config['LANGUAGES']
        ,CURRENT_LANGUAGE=session.get('language',request.accept_languages.best_match(app.config['LANGUAGES'].keys()))
        ,DEFAULT_LANGUAGE=app.config['DEFAULT_LANGUAGE']
        ,FLAGS=app.config['FLAGS']
        ,COPYWRITE_YEAR=app.config['COPYWRITE_YEAR']
        ,WEBSITE_TITLE=app.config['DOMAIN_TITLE']
        ,COMPANY_NAME = app.config['COMPANY_NAME']
        ,DOMAIN_NAME=app.config['DOMAIN_NAME']
        ,DOMAIN_TITLE =app.config['DOMAIN_TITLE']
        ,COMPANY_COLOR=app.config['COMPANY_COLOR']
        ,DOMAIN_COLOR=app.config['DOMAIN_COLOR']
        ,COMPANY_ADDRESS=app.config['COMPANY_ADDRESS']
        ,COMPANY_PHONES=app.config['COMPANY_PHONES']
        ,COMPANY_CONTACT_EMAIL=app.config['COMPANY_CONTACT_EMAIL']
        ,COMPANY_SUPPORT_EMAIL=app.config['COMPANY_SUPPORT_EMAIL']
        ,CONTACT_EMAIL=app.config['CONTACT_EMAIL']
        ,SUPPORT_EMAIL=app.config['SUPPORT_EMAIL']
        ,INQUIRY_EMAIL=app.config['INQUIRY_EMAIL']
        ,WEBSITE_ADMIN_EMAIL=app.config['WEBSITE_ADMIN_EMAIL']
        #variables required for splash
        ,homepage_html = app.homepage_html
        ,loginform=app.loginform
        ,registrationform=app.registrationform
        ,contactusform=app.contactusform
        ,forgetpasswordform=app.forgetpasswordform
        ,cookiesconsentform=app.cookiesconsentform
        ,SPLASHFORM_LOGIN = app.config['SPLASHFORM_LOGIN']
        ,SPLASHFORM_REGISTRATION = app.config['SPLASHFORM_REGISTRATION']
        ,SPLASHFORM_FORGETPASSWORD = app.config['SPLASHFORM_FORGETPASSWORD']
        ,SPLASHFORM_CONTACTUS = app.config['SPLASHFORM_CONTACTUS']
)

@app.context_processor
def inject_utility_functions():
    #log_info('###SERVER_RUNNING###','inject_utility_functions:')
    #log_info('###inject_utility_functions:format_price()')
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)

    #log_info('###inject_utility_functions:language_file()')
    def language_file(file='',language='en'):
        nfile=file
        if (language not in app.config['LANGUAGES']):
            language=app.config['DEFAULT_LANGUAGE']
        if (language!=app.config['DEFAULT_LANGUAGE']):
            nfile=file.replace('.html', '_'+language+'.html')
        return nfile

    #log_info('###inject_utility_functions:version_file()')
    def version_file(file='',environment='',design='',version=''):
        nfile=file
        if (environment!=''):
            nfile=environment+content_page+nfile
        if (design!=''):
            nfile=nfile.replace('.', '_'+design+'.')
        if (version!=''):
            nfile=nfile.replace('.', '_v'+version+'.')
        return nfile

    def appfolder(type='template',module=''):
        folder=app.config['TEMPLATES_ROOT_FOLDER']
        folder=''
        if module:
            folder=module+'/'

        if (type.upper()=='MASTERLAYOUT' or type.upper()=='MASTER_LAYOUT' or type.upper()=='PAGESLAYOUT' or type.upper()=='PAGE_LAYOUT'):
            folder=folder
        if (type.upper()=='LAYOUT'):
            folder=folder+app.config['LAYOUTS_FOLDER']
        if (type.upper()=='LAYOUT_COMPONENT'):
            folder=folder+app.config['LAYOUTS_FOLDER']
        if (type.upper()=='TEMPLATE'):
            folder=folder+app.config['TEMPLATES_FOLDER']
        if (type.upper()=='PAGE'):
            folder=folder+app.config['PAGES_FOLDER']
        if (type.upper()=='COMPONENT'):
            folder=folder+app.config['COMPONENTS_FOLDER']
        if (type.upper()=='IMAGE'):
            folder=folder+app.config['IMAGES_FOLDER']
        if (type.upper()=='PICTURE'):
            folder=folder+app.config['PICTURES_FOLDER']
        if (type.upper()=='VIDEO'):
            folder=folder+app.config['VIDEOS_FOLDER']
        if (type.upper()=='FORM'):
            folder=folder+app.config['FORMS_FOLDER']
        # if module:
        #     if (type.upper()=='LAYOUT_COMPONENT' or type.upper()=='TEMPLATE' or not(type)):
        #         folder=module+'/'

        return folder


    #log_info('###inject_utility_functions:fullpathfile()')
    def fullpathfile(file='',type='TEMPLATE',module=''):
        folder=appfolder(type,module)
        file1=file
        file2=file1
        if not os.path.dirname(file1):
            file2=os.path.join(folder,file1)
            file2=os.path.normpath(file2)
            file2=file2.replace('\\','/')
        return file2

    #log_info('###inject_utility_functions:include_files()')
    def include_files(file='',type='TEMPLATE',module='',language='en'):
        file_extension = os.path.splitext(file)[1]
        file_extension = file_extension.lower()
        if file_extension not in ['.html']:
            if file_extension in ['.bmp','.png','.gif','.tiff']:
                type = 'IMAGES'
            if file_extension in ['.mp4']:
                type = 'VIDEOS'
        #print('module',module)
        #folder from type,module
        folder=appfolder(type,module)
        rootfolder=appfolder(type,'')
        #print('folder=',folder,rootfolder)
        file1=file
        if not os.path.dirname(file):
            file1=os.path.join(folder,file)
            #if module != '':
            rootfile1=os.path.join(rootfolder,file)
        #print('f1=',file1,rootfile1)
        file2=file1
        rootfile2=rootfile1
        file3=file1
        rootfile3=rootfile1
        file4=file1
        rootfile4=rootfile1
        if (language not in app.config['LANGUAGES']):
            language=app.config['DEFAULT_LANGUAGE']
        if (language!=app.config['DEFAULT_LANGUAGE']):
            filename=os.path.basename(file1)
            justfile=os.path.splitext(filename)[0]
            justext=os.path.splitext(filename)[1]
            Njustfile=justfile+'_'+language
            Nfilename=Njustfile+justext
            file2x=os.path.join(os.path.dirname(file1),Nfilename)
            file2x=os.path.normpath(file2x)
            file2x=file2x.replace('\\','/')
            file2=file2x
            #if module != '':
            file2x=os.path.join(os.path.dirname(rootfile1),Nfilename)
            file2x=os.path.normpath(file2x)
            file2x=file2x.replace('\\','/')
            rootfile2=file2x
            #print('f2(lang)=',file2,rootfile2)

        if type in app.config['DEBUG_TYPES'] or '*' in app.config['DEBUG_TYPES'] :
            if app.config['EXECUTION_MODE'] != 'production':
                filename=os.path.basename(file1)
                justfile=os.path.splitext(filename)[0]
                justext=os.path.splitext(filename)[1]
                Njustfile=justfile+'_'+app.config['EXECUTION_MODE']
                Nfilename=Njustfile+justext
                file2x=os.path.join(os.path.dirname(file1),Nfilename)
                file2x=os.path.normpath(file2x)
                file2x=file2x.replace('\\','/')
                file3=file2x
                #if module != '':
                file2x=os.path.join(os.path.dirname(rootfile1),Nfilename)
                file2x=os.path.normpath(file2x)
                file2x=file2x.replace('\\','/')
                rootfile3=file2x
                #print('f3(mode)=',file3,rootfile3)

        if app.config['DEBUG_VERSION'] != '' :
            filename=os.path.basename(file1)
            justfile=os.path.splitext(filename)[0]
            justext=os.path.splitext(filename)[1]
            Njustfile=justfile+'_v'+app.config['DEBUG_VERSION']
            Nfilename=Njustfile+justext
            file2x=os.path.join(os.path.dirname(file1),Nfilename)
            file2x=os.path.normpath(file2x)
            file2x=file2x.replace('\\','/')
            file4=file2x
            #if module != '':
            file2x=os.path.join(os.path.dirname(rootfile1),Nfilename)
            file2x=os.path.normpath(file2x)
            file2x=file2x.replace('\\','/')
            rootfile4=file2x
            #print('f4(version)=',file4,rootfile4)

        x=[]
        if file4 != file1:
            x.append(file4)
            if rootfile4 != file4:
                x.append(rootfile3)
        if file3 != file1:
            x.append(file3)
            if rootfile3 != file3:
                x.append(rootfile3)
        if file2 != file1:
            x.append(file2)
            if rootfile2 != file2:
                x.append(rootfile2)
        x.append(file1)
        if rootfile1 != file1:
            x.append(rootfile1)
        #if app.config.get('DEBUG_INCLUDES') \
        if os.environ.get('DEBUG_INCLUDE') in ('ON', True) :
            print('###include_files###=',x)
        return x

    #log_info('###inject_utility_functions:image_file()')
    def image_file(file=''):
        file1=file
        file2=file1
        if not os.path.dirname(file1):
            file2=os.path.join(app.config['IMAGES_FOLDER'],file1)
            file2=os.path.normpath(file2)
            file2=file2.replace('\\','/')
        return file2

    #log_info('###inject_utility_functions:video_file()')
    def video_file(file=''):
        file1=file
        file2=file1
        if not os.path.dirname(file1):
            file2=os.path.join(app.config['VIDEOS_FOLDER'],file1)
            file2=os.path.normpath(file2)
            file2=file2.replace('\\','/')
        return file2

    #log_info('###inject_utility_functions:picture_file()')
    def picture_file(file=''):
        file1=file
        file2=file1
        if not os.path.dirname(file1):
            file2=os.path.join(app.config['PICTURES_FOLDER'],file1)
            file2=os.path.normpath(file2)
            file2=file2.replace('\\','/')
        return file2

    #log_info('###inject_utility_functions:flag_file()')
    def flag_file(file=''):
        file1=file
        file2=file1
        if not os.path.dirname(file1):
            file2=os.path.join(app.config['FLAGS_FOLDER'],file1)
            file2=os.path.normpath(file2)
            file2=file2.replace('\\','/')
        return file2

    #log_info('###inject_utility_functions:page_file()')
    def page_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['PAGES_FOLDER']+file1
            else:
                file2 = app.config['PAGES_FOLDER']+file1
        return file2

    #log_info('###inject_utility_functions:form_file()')
    def form_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['FORMS_FOLDER']+file1
            else:
                file2 = app.config['FORMS_FOLDER']+file1
        return file2

    #log_info('###inject_utility_functions:component_file()')
    def component_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['COMPONENTS_FOLDER']+file1
            else:
                file2 = app.config['COMPONENTS_FOLDER']+file1
        return file2

    #log_info('###inject_utility_functions:template_file()')
    def template_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+file1
            else:
                file2 = app.config['TEMPLATES_FOLDER']+file1
        return file2

    #log_info('###inject_utility_functions:layout_file()')
    def layout_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            folder=appfolder('LAYOUT_COMPONENT',module)
            file2 = folder+file1
        return file2

    #log_info('###inject_utility_functions:email_template_file()')
    def email_template_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['EMAILS_FOLDER']+file1
            else:
                file2 = app.config['EMAILS_FOLDER']+file1
        return file2

    #log_info('###inject_utility_functions:sms_template_file()')
    def sms_template_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['SMS_FOLDER']+file1
            else:
                file2 = app.config['SMS_FOLDER']+file1
        return file2


    #log_info('###inject_utility_functions:language_page_file()')
    def language_page_file(file='',language='en',module=''):
        nfile=page_file(file,module)
        if (language not in app.config['LANGUAGES']):
            language=app.config['DEFAULT_LANGUAGE']
        if (language!=app.config['DEFAULT_LANGUAGE']):
            nfile=nfile.replace('.html', '_'+language+'.html')
        return nfile


    #log_info('###inject_utility_functions:language_fullpathfile()')
    def language_fullpathfile(file='',language='en',type='PAGE',module=''):
        nfile=fullpathfile(file,type,module)
        if (language not in app.config['LANGUAGES']):
            language=app.config['DEFAULT_LANGUAGE']
        if (language!=app.config['DEFAULT_LANGUAGE']):
            nfile=nfile.replace('.html', '_'+language+'.html')
        return nfile

    #log_info('###inject_utility_functions:language_fullpathfile()')
    #def cookies_consent():
    #    return session.get('cookies_consent')

    return dict(
        format_price=format_price
        ,appfolder=appfolder
        ,fullpathfile=fullpathfile
        ,language_file=language_file
        ,language_fullpathfile=language_fullpathfile
        ,version_file=version_file
        ,image_file=image_file
        ,picture_file=picture_file
        ,video_file=video_file
        ,flag_file=flag_file
        ,layout_file=layout_file
        ,template_file=template_file
        ,component_file=component_file
        ,page_file=page_file
        ,language_page_file=language_page_file
        ,form_file=form_file
        ,email_template_file=email_template_file
        ,sms_template_file=sms_template_file
        ,include_files=include_files
)
#log_finish('###FUNCTIONS & VARIABLES###')
################################################################################
################################################################################
################################################################################
## epiloque
################################################################################
################################################################################
#log_start('config_checkpoint_3')
log_checkpoint('3', '###SQLALCHEMY_POOL_RECYCLE####', app.config['SQLALCHEMY_POOL_RECYCLE'])
log_checkpoint('3', '###SQLALCHEMY_POOL_TIMEOUT####', app.config['SQLALCHEMY_POOL_TIMEOUT'])
log_checkpoint('3', '###SQLALCHEMY_POOL_SIZE####', app.config['SQLALCHEMY_POOL_SIZE'])
#print('####################db.pool_recycle########',db.pool_recycle)
#log_finish('config_checkpoint_3')
################################################################################
log_info('###FINISHED: FLASK-APP:CREATED-CONFIG-READY###')
################################################################################
log_init_finish(__file__,'app_init')
################################################################################

################################################################################
################################################################################
################################################################################
## application debug_config
################################################################################
################################################################################
debug_config_execution()
if app.config.get('EXECUTION_MODE') in ('sandbox', 'production'):
    set_global_debug('OFF')
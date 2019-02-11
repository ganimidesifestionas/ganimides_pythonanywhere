# myApp/__init__.py
"""
The flask application package.
"""
import os
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
from .config import app_config

#from logging.config import dictConfig
#from .external_services.log_services import *
#print('   ',__name__,'###dictConfig###', dictConfig)

#################logging#######
#logging config
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
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
logger.info('Hello World!!!')

# def create_app():
#     app = Flask(__name__)
#     db.init_app(app)
#     return app
################################################################################
################################################################################
################################################################################
### Define the WSGI application object
################################################################################
################################################################################
################################################################################
print('   ',__name__,'#############################################################')
print('   ',__name__,'###CREATE FLASK-APP###','app = Flask(__name__, instance_relative_config=True)')
app = Flask(__name__, instance_relative_config=True)
#--> important: the folders are relative to where the flask app is created
# specifies the main template folder for the application
#app = Flask(__name__,
#            instance_path=get_instance_folder_path(),
#            instance_relative_config=True,
#            template_folder='templates')
#print('   ',__name__,'###SQLALCHEMY_POOL_RECYCLE####', app.config['SQLALCHEMY_POOL_RECYCLE'])
################################################################################
################################################################################
################################################################################
### app variables
################################################################################
################################################################################
################################################################################
#required for splash forms: will be set in @app.before_first_request
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
print('   ',__name__,'Start')
##-##-####-##-####-##-####-##-####-##-##
################################################################################
################################################################################
################################################################################
### app flask config
################################################################################
################################################################################
################################################################################
print('   ',__name__,'###app###','app.instance_path = ',app.instance_path)
print('   ',__name__,'###app###','app.template_folder =',app.template_folder)
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
print('   ',__name__,'###app###','FLASK_CONFIGURATION =',config_name)
# enable jinja2 extensions - i.e. continue in for loops
#app.jinja_env.add_extension('jinja2.ext.loopcontrols')
#...
################################################################################
################################################################################
################################################################################
### Configurations
################################################################################
################################################################################
################################################################################
#print('   ',__name__,'')
print('   ',__name__,'###CONFIGURE FLASK-APP###')
#########################################################################################
print('   ',__name__,'   CONFIG-1-FROM-SERVER','../server_config.py')
app.config.from_pyfile('../server_config.py') #from the (server) root
#print('   ',__name__,'   (1-server) EYECATCH---',app.config['EYECATCH'])
#print('   ',__name__,'   (1-server) SERVER---',app.config['SERVER'])
#print('   ',__name__,'   (1-server) SQLALCHEMY_DATABASE_URI---',app.config['SQLALCHEMY_DATABASE_URI'])
#########################################################################################
print('   ',__name__,'   CONFIG-2-FROM-SERVER-INSTANCE','../instance/config.py')
app.config.from_pyfile('../instance/config.py') #from instance
#print('   ',__name__,'   (2-instance) EYECATCH---',app.config['EYECATCH'])
#print('   ',__name__,'   (2-instance) SQLALCHEMY_DATABASE_URI---',app.config['SQLALCHEMY_DATABASE_URI'])
#########################################################################################
config_name = app.config['EXECUTION_ENVIRONMENT']
print('   ',__name__,'   CONFIG-3-APP-ENVIRONMENT',config_name,'.config.py')
app.config.from_object(app_config[config_name])
print('   ',__name__,'   (3-environment)',config_name,'EYECATCH---',app.config['EYECATCH'])
#print('   ',__name__,'   (3-environment)',config_name,'SQLALCHEMY_DATABASE_URI---',app.config['SQLALCHEMY_DATABASE_URI'])
#########################################################################################
config_name = app.config['EXECUTION_MODE']
print('   ',__name__,'   CONFIG-4-APP-EXEC-MODE',config_name,'.config.py')
app.config.from_object(app_config[config_name])
print('   ',__name__,'   (4-exec-mode)',config_name,'EYECATCH---',app.config['EYECATCH'])
#print('   ',__name__,'   (4-exec-mode)',config_name,'SQLALCHEMY_DATABASE_URI---',app.config['SQLALCHEMY_DATABASE_URI'])
#########################################################################################

#########################################################################################
print('   ',__name__,'   @@@check', 'SERVER---',app.config['SERVER'])
print('   ',__name__,'   @@@check', 'DATABASE_SERVER---',app.config['DATABASE_SERVER'])
print('   ',__name__,'   @@@check', 'DATABASE_NAME---',app.config['DATABASE_NAME'])
print('   ',__name__,'   @@@check', 'DATABASE_SERVER_URI---',app.config['DATABASE_SERVER_URI'])
print('   ',__name__,'   @@@check', 'DATABASE_URI---',app.config['DATABASE_URI'])
print('   ',__name__,'   @@@check', 'SQLALCHEMY_DATABASE_URI---',app.config['SQLALCHEMY_DATABASE_URI'])
print('   ',__name__,'   @@@check', 'SQLALCHEMY_DATABASE_URI---',app.config['SQLALCHEMY_DATABASE_URI'])
print('   ',__name__,'   @@@check', 'RECAPTCHA_SITE_KEY---',app.config['RECAPTCHA_SITE_KEY'])
print('   ',__name__,'   @@@check', 'RECAPTCHA_SECRET_KEY---',app.config['RECAPTCHA_SECRET_KEY'])
print('   ',__name__,'   @@@check', 'SPLASH FORM---',app.config['SPLASHFORM_LOGIN'])
print('   ',__name__,'   @@@check', 'SPLASH FORM---',app.config['SPLASHFORM_REGISTRATION'])
print('   ',__name__,'   @@@check', 'SPLASH FORM---',app.config['SPLASHFORM_FORGETPASSWORD'])
print('   ',__name__,'   @@@check', 'SPLASH FORM---',app.config['SPLASHFORM_CONTACTUS'])
################################################################################
################################################################################
################################################################################
### ?????????????
################################################################################
################################################################################
################################################################################
#print('   ',__name__,'')
print('   ',__name__,'###BOOTSTRAP APP###','Bootstrap(app)')
Bootstrap(app)
################################################################################
################################################################################
################################################################################
### Define the database object which is imported by modules and controllers
################################################################################
################################################################################
################################################################################
print('   ',__name__,'###DATABASE###','define database:db = SQLAlchemy(app)')
db = SQLAlchemy()
db.init_app(app)
################################################################################
################################################################################
################################################################################
### LoginManager
################################################################################
################################################################################
################################################################################
#print('   ',__name__,'')
print('   ',__name__,'###LOGIN-MANAGER###','login_manager = LoginManager(application)')
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
#print('   ',__name__,'')
print('   ',__name__,'###Migration-MANAGER###')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
#manager.run(db)
################################################################################
################################################################################
################################################################################
### Home page
################################################################################
################################################################################
################################################################################
#print('   ',__name__,'')
#print('   ',__name__,'###HOME_PAGE###',"render_template('page_templates/landing_page.html',title='landing page')")
#@app.route('/')
#def landingpage():
#    print('   ',__name__,'LANDINGPAGE',request.method,request.url)
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
#print('   ',__name__,'')
print('   ',__name__,'###ERROR_HANDLERS###')
print('   ',__name__,'   @app.errorhandler(403)','render_template(error_pages/403.html, title=Forbidden)')
@app.errorhandler(403)
def forbidden(error):
    return render_template('error_pages/403.html', title='Forbidden'), 403

print('   ',__name__,'   @app.errorhandler(404)','render_template(error_pages/404.html, title=Page Not Found)')
@app.errorhandler(404)
def page_not_found(error):
    varPageName = str(request._get_current_object())
    return render_template('error_pages/404.html', title='Page Not Found',PageNotFound=varPageName), 404

print('   ',__name__,'   @app.errorhandler(500)','render_template(error_pages/500.html, title=Server Error)')
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error_pages/500.html', title='Server Error'), 500

################################################################################
################################################################################
################################################################################
# import home pages
################################################################################
################################################################################
################################################################################
print('   ',__name__,'###HOME PAGES###')
from . import views
################################################################################
################################################################################
################################################################################
# Register blueprint(s) for pages
################################################################################
################################################################################
################################################################################
#print('   ',__name__,'')
print('   ',__name__,'###BLUEPRINTS (SUB-APPCOMPONENTS)###')
# Import modules/components using their blueprint handler variable i.e module_authoroization

### authorization module
from . module_authorization.routes import authorization as authorization_module
app.register_blueprint(authorization_module, url_prefix='/authorization')
print('   ',__name__,'   authorization_module---','app.register_blueprint(authorization_module,url_prefix=''/authorization'')')

### administration module
from . module_administration.routes import administration as administration_module
app.register_blueprint(administration_module, url_prefix='/administration')
print('   ',__name__,'   administration_module---','app.register_blueprint(administration_module,url_prefix=''/administration'')')

### protototypes page
#from . module_prototypes.controllers import prototypes as prototypes_module
#app.register_blueprint(prototypes_module,url_prefix='/prototypes')
#print('   ',__name__,'   prototypes_module---','app.register_blueprint(prototypes_module,url_prefix=''/prototypes'')')

#from app import models
#from .admin import admin as admin_blueprint
#app.register_blueprint(admin_blueprint, url_prefix='/admin')
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
print('   ')
print('   ',__name__,'###DATABASE###','create database if not exists')
#create the database if not exists
SERVER = app.config['SERVER'] # application server
DATABASE_SERVER = app.config['DATABASE_SERVER']
DATABASE_NAME = app.config['DATABASE_NAME']
DATABASE_URI=app.config['SQLALCHEMY_DATABASE_URI']
DATABASE_SERVER_URI=app.config['DATABASE_SERVER_URI']
DB_URI=app.config['DATABASE_URI']

dbserver_engine = sqlalchemy.create_engine(DATABASE_SERVER_URI,pool_recycle=180) # connect to server
existing_databases = dbserver_engine.execute("SHOW DATABASES;")
existing_databases = [d[0] for d in existing_databases]
# for database in existing_databases:
#     print("...database {0} on dbserver {1}".format(database, DATABASE_SERVER_URI))
if DATABASE_NAME not in existing_databases:
    dbserver_engine.execute("CREATE DATABASE {db}".format(db=DATABASE_NAME))
    print('   ',__name__,'###DATABASE###',"   {0} database CREATED on DBserver {1}".format(DATABASE_NAME, DATABASE_SERVER))
else:
    print('   ',__name__,'###DATABASE###',"   database {0} already exists on DBserver {1}".format(DATABASE_NAME, DATABASE_SERVER))
# -or-
# dbserver_engine.execute("CREATE DATABASE IF NOT EXISTS {db}".format(db=DATABASE_NAME))
# dbserver_engine.execute("USE {db}".format(db=DATABASE_NAME))
#dbserver_engine.dispose()
dbserver_engine.execute("USE {db}".format(db=DATABASE_NAME))
dbserver_engine.dispose()

print('   ',__name__,'###DATABASE###','create tables if not exists')
from .module_administration.models import User, Department, Role
from .module_authorization.models import Subscriber, ContactMessage
from .models import Visit, VisitPoint, Page_Visit

# recreate tables etc
print('   ',__name__,'###DATABASE###','db.create_all(app=app)')
db_engine = sqlalchemy.create_engine(DATABASE_URI, pool_recycle=180) # connect to database
existing_tables_before = db_engine.execute('SHOW TABLES;')
existing_tables_before = [d[0] for d in existing_tables_before]
#print('   ', 'database-init', __name__, 'tables before')
#list_tables(db_engine)

db.create_all(app=app)
#db.session.commit()

existing_tables_after = db_engine.execute('SHOW TABLES;')
existing_tables_after = [d[0] for d in existing_tables_after]
created = 0
for table in existing_tables_after:
    if table not in existing_tables_before:
        created = created + 1

db_engine.dispose()
print('   ',__name__,'###DATABASE###',"   {0} tables created in database {1}".format(created,DATABASE_NAME))

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
#print('   ',__name__,'')
print('   ',__name__,'###FUNCTIONS & VARIABLES###')
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
    print('   ',__name__,'###SERVER_APP_RUNNING###','@app.teardown_appcontext:','db_session.remove()')
    #db.db_session.remove()

@app.context_processor
def inject_configuration_parameters_as_variables():
    #print('   ',__name__,'###SERVER_APP_RUNNING###','inject_configuration_parameters_as_variables:')
    #print('   ', '!!! splash forms objects made available by the server...')
    return dict(
        EXECUTION_MODE=app.config['EXECUTION_MODE']
        ,SERVER = app.config['SERVER'] # application server
        ,DATABASE_SERVER = app.config['DATABASE_SERVER']
        ,DATABASE_NAME = app.config['DATABASE_NAME']
        ,DATABASE_URI=app.config['SQLALCHEMY_DATABASE_URI']
        ,DATABASE_SERVER_URI=app.config['DATABASE_SERVER_URI']
        ,DB_URI=app.config['DATABASE_URI']
        ,RECAPTCHA_SITE_KEY=app.config['RECAPTCHA_SITE_KEY']
        ,RECAPTCHA_SECRET_KEY=app.config['RECAPTCHA_SECRET_KEY']
        ,RECAPTCHA_PUBLIC_KEY=app.config['RECAPTCHA_SITE_KEY']
        ,RECAPTCHA_PRIVATE_KEY=app.config['RECAPTCHA_SECRET_KEY']
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
    #print('   ',__name__,'###SERVER_RUNNING###','inject_utility_functions:')
    #print('   ',__name__,'###inject_utility_functions:format_price()')
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)

    #print('   ',__name__,'###inject_utility_functions:language_file()')
    def language_file(file='',language='en'):
        nfile=file
        if (language not in app.config['LANGUAGES']):
            language=app.config['DEFAULT_LANGUAGE']
        if (language!=app.config['DEFAULT_LANGUAGE']):
            nfile=file.replace('.html', '_'+language+'.html')
        return nfile

    #print('   ',__name__,'###inject_utility_functions:version_file()')
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

        if (type.upper()=='MASTERLAYOUT' or type.upper()=='PAGESLAYOUT'):
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
        if (type.upper()=='FORM'):
            folder=folder+app.config['FORMS_FOLDER']
        # if module:
        #     if (type.upper()=='LAYOUT_COMPONENT' or type.upper()=='TEMPLATE' or not(type)):
        #         folder=module+'/'

        return folder


    #print('   ',__name__,'###inject_utility_functions:fullpathfile()')
    def fullpathfile(file='',type='TEMPLATE',module=''):
        folder=appfolder(type,module)
        # folder=app.config['TEMPLATES_ROOT_FOLDER']
        # if (type.upper()=='LAYOUT_COMPONENT'):
        #     folder=app.config['LAYOUTS_FOLDER']
        # if (type.upper()=='TEMPLATE'):
        #     folder=app.config['TEMPLATES_FOLDER']
        # if (type.upper()=='PAGE'):
        #     folder=app.config['PAGES_FOLDER']
        # if (type.upper()=='COMPONENT'):
        #     folder=app.config['COMPONENTS_FOLDER']
        # if (type.upper()=='IMAGE'):
        #     folder=app.config['IMAGES_FOLDER']
        # if (type.upper()=='PICTURE'):
        #     folder=app.config['PICTURES_FOLDER']
        # if (type.upper()=='FORM'):
        #     folder=app.config['FORMS_FOLDER']

        # if module:
        #     if (type.upper()=='LAYOUT_COMPONENT'):
        #         folder=module+'/'
        #     else:
        #         folder=module+'/'+folder

        file1=file
        file2=file1
        if (file1.find('/')<0):
            file2 = folder+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:image_file()')
    def image_file(file=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            file2 = app.config['IMAGES_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:picture_file()')
    def picture_file(file=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            file2 = app.config['PICTURES_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:flag_file()')
    def flag_file(file=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            file2 = app.config['FLAGS_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:page_file()')
    def page_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['PAGES_FOLDER']+file1
            else:
                file2 = app.config['PAGES_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:form_file()')
    def form_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['FORMS_FOLDER']+file1
            else:
                file2 = app.config['FORMS_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:component_file()')
    def component_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['COMPONENTS_FOLDER']+file1
            else:
                file2 = app.config['COMPONENTS_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:template_file()')
    def template_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+file1
            else:
                file2 = app.config['TEMPLATES_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:layout_file()')
    def layout_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            folder=appfolder('LAYOUT_COMPONENT',module)
            file2 = folder+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:email_template_file()')
    def email_template_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['EMAILS_FOLDER']+file1
            else:
                file2 = app.config['EMAILS_FOLDER']+file1
        return file2

    #print('   ',__name__,'###inject_utility_functions:sms_template_file()')
    def sms_template_file(file='',module=''):
        file1=file
        file2=file1
        if (file1.find('/')<0):
            if module:
                file2 = module+'/'+app.config['SMS_FOLDER']+file1
            else:
                file2 = app.config['SMS_FOLDER']+file1
        return file2


    #print('   ',__name__,'###inject_utility_functions:language_page_file()')
    def language_page_file(file='',language='en',module=''):
        nfile=page_file(file,module)
        if (language not in app.config['LANGUAGES']):
            language=app.config['DEFAULT_LANGUAGE']
        if (language!=app.config['DEFAULT_LANGUAGE']):
            nfile=nfile.replace('.html', '_'+language+'.html')
        return nfile


    #print('   ',__name__,'###inject_utility_functions:language_fullpathfile()')
    def language_fullpathfile(file='',language='en',type='PAGE',module=''):
        nfile=fullpathfile(file,type,module)
        if (language not in app.config['LANGUAGES']):
            language=app.config['DEFAULT_LANGUAGE']
        if (language!=app.config['DEFAULT_LANGUAGE']):
            nfile=nfile.replace('.html', '_'+language+'.html')
        return nfile

    #print('   ',__name__,'###inject_utility_functions:language_fullpathfile()')
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
        ,flag_file=flag_file
        ,layout_file=layout_file
        ,template_file=template_file
        ,component_file=component_file
        ,page_file=page_file
        ,language_page_file=language_page_file
        ,form_file=form_file
        ,email_template_file=email_template_file
        ,sms_template_file=sms_template_file
        #,cookies_consent=cookies_consent
)
################################################################################
################################################################################
################################################################################
## epiloque
################################################################################
################################################################################
print('   ',__name__,'###SQLALCHEMY_POOL_RECYCLE####', app.config['SQLALCHEMY_POOL_RECYCLE'])
print('   ',__name__,'###SQLALCHEMY_POOL_TIMEOUT####', app.config['SQLALCHEMY_POOL_TIMEOUT'])
print('   ',__name__,'###SQLALCHEMY_POOL_SIZE####', app.config['SQLALCHEMY_POOL_SIZE'])
print('   ',__name__,'###FINISHED: FLASK-APP-created&ready###')
print('   ',__name__,'#############################################################')
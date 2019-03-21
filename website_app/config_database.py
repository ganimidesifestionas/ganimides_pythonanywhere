"""database configurations database_config.py"""
import os
from website_app.debug_services.debug_log_services import *

log_module_start('database_configuration')

EYECATCH = 'DATABASE'

#os.environ[COMPANY_NAME+'_'+APPLICATION_NAME+'_'+'EXECUTION_ENVIRONMENT']='pythonanywhere'
#####################################################################
EXECUTION_ENVIRONMENT = os.environ.get('EXECUTION_ENVIRONMENT').replace("'", '')
EXECUTION_MODE = os.environ.get('EXECUTION_MODE').replace("'", '')
SERVER = os.environ.get('SERVER').replace("'", '')
DATABASE_SERVER = os.environ.get('DATABASE_SERVER').replace("'", '')
DATABASE_NAME = os.environ.get('DATABASE_NAME').replace("'", '')
DATABASE_USER = os.environ.get('DATABASE_USER').replace("'", '')
DATABASE_PASS = os.environ.get('DATABASE_PASS').replace("'", '')
DATABASE_CONNECTION_PREFIX = os.environ.get('DATABASE_CONNECTION_PREFIX').replace("'", '')
if not DATABASE_SERVER:
   DATABASE_SERVER = 'localhost'
if not SERVER:
   SERVER = 'localhost'
if not EXECUTION_ENVIRONMENT:
    EXECUTION_ENVIRONMENT = 'localhost'
if not DATABASE_CONNECTION_PREFIX:
    DATABASE_CONNECTION_PREFIX = 'mysql+pymysql://'
#####################################################################
if EXECUTION_ENVIRONMENT == 'localhost':
    if not EXECUTION_MODE:
        EXECUTION_MODE = 'design'
    if not SERVER:
        SERVER = 'localhost'
    if not DATABASE_SERVER:
        DATABASE_SERVER = 'localhost'
    if not DATABASE_NAME:
        DATABASE_NAME = 'ifestionas_db'
else:
    if EXECUTION_ENVIRONMENT == 'pythonanywhere':
        if not EXECUTION_MODE:
            EXECUTION_MODE = 'production'
        if not SERVER:
            SERVER = 'pythonanywhere'
        if not DATABASE_SERVER:
            DATABASE_SERVER = 'ganimedes.mysql.pythonanywhere-services.com'
        if not DATABASE_NAME:
            DATABASE_NAME = 'ifestionas$ganimides_db'
    else:
        if not EXECUTION_MODE:
            EXECUTION_MODE = 'testing'
        if not SERVER:
            SERVER = 'heroku'
        if not DATABASE_SERVER:
            DATABASE_SERVER = 'ganimedes.mysql.pythonanywhere-services.com'
        if not DATABASE_NAME:
            DATABASE_NAME = 'ifestionas$ganimides_db'

################################################################
### database connections
################################################################
#dialect+driver://username:password@host:port/database

#server:localhost , database:ifestionas_db
localhost_DATABASE_HOST_ADDRESS = 'localhost'
localhost_DATABASE_NAME = 'ifestionas_db'
localhost_DATABASE_USER = 'ganimedes'
localhost_DATABASE_PASS = 'philea13'
localhost_DATABASE_CONNECTION_PREFIX = 'mysql+pymysql://'
localhost_DATABASE_SERVER = localhost_DATABASE_HOST_ADDRESS
localhost_DATABASE_SERVER_URI = localhost_DATABASE_CONNECTION_PREFIX + localhost_DATABASE_USER+':'+localhost_DATABASE_PASS+'@'+localhost_DATABASE_HOST_ADDRESS
localhost_DATABASE_URI = localhost_DATABASE_SERVER_URI+'/'+localhost_DATABASE_NAME
localhost_SQLALCHEMY_DATABASE_URI = localhost_DATABASE_URI

#server:pythonanywhere , database:ganimedes_db
pythonanywhere_ganimedes_DATABASE_HOST_ADDRESS = 'ganimedes.mysql.pythonanywhere-services.com'
pythonanywhere_ganimedes_DATABASE_NAME = 'ganimedes$ganimides_db'
pythonanywhere_ganimedes_DATABASE_USER = 'ganimedes'
pythonanywhere_ganimedes_DATABASE_PASS = 'philea13'
pythonanywhere_ganimedes_DATABASE_CONNECTION_PREFIX = 'mysql+pymysql://'
pythonanywhere_ganimedes_DATABASE_SERVER = pythonanywhere_ganimedes_DATABASE_HOST_ADDRESS
pythonanywhere_ganimedes_DATABASE_SERVER_URI = pythonanywhere_ganimedes_DATABASE_CONNECTION_PREFIX+pythonanywhere_ganimedes_DATABASE_USER+':'+pythonanywhere_ganimedes_DATABASE_PASS+'@'+pythonanywhere_ganimedes_DATABASE_HOST_ADDRESS
pythonanywhere_ganimedes_DATABASE_URI = pythonanywhere_ganimedes_DATABASE_SERVER_URI+'/'+pythonanywhere_ganimedes_DATABASE_NAME
pythonanywhere_ganimedes_SQLALCHEMY_DATABASE_URI = pythonanywhere_ganimedes_DATABASE_URI

#server:pythonanywhere , database:ifestionas_db
pythonanywhere_ifestionas_DATABASE_HOST_ADDRESS = 'ifestionas.mysql.pythonanywhere-services.com'
pythonanywhere_ifestionas_DATABASE_NAME = 'ifestionas$ganimides_db'
pythonanywhere_ifestionas_DATABASE_USER = 'ifestionas'
pythonanywhere_ifestionas_DATABASE_PASS = 'philea13'
pythonanywhere_ifestionas_DATABASE_CONNECTION_PREFIX = 'mysql+pymysql://'
pythonanywhere_ifestionas_DATABASE_SERVER = pythonanywhere_ifestionas_DATABASE_HOST_ADDRESS
pythonanywhere_ifestionas_DATABASE_SERVER_URI = pythonanywhere_ifestionas_DATABASE_CONNECTION_PREFIX+pythonanywhere_ifestionas_DATABASE_USER+':'+pythonanywhere_ifestionas_DATABASE_PASS+'@'+pythonanywhere_ifestionas_DATABASE_HOST_ADDRESS
pythonanywhere_ifestionas_DATABASE_URI = pythonanywhere_ifestionas_DATABASE_SERVER_URI+'/'+pythonanywhere_ifestionas_DATABASE_NAME
pythonanywhere_ifestionas_SQLALCHEMY_DATABASE_URI = pythonanywhere_ifestionas_DATABASE_URI

#pythonanywhere_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ifestionas:philea13@ifestionas.mysql.pythonanywhere-services.com/ifestionas$ganimides_db'
#DATABASE_URI=                             'mysql+pymysql://''ifestionas':'philea13'@'ganimedes.mysql.pythonanywhere-services.com'/'ifestionas$ganimides_db' [config]
#pythonanywhere_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db'
#localhost_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ifestionas_db'
#localhost_SQLALCHEMY_TEST_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimedes_db_test'

#default is localhost
# DATABASE_HOST_ADDRESS = localhost_DATABASE_HOST_ADDRESS
# DATABASE_NAME = localhost_DATABASE_NAME
# DATABASE_USER = localhost_DATABASE_USER
# DATABASE_PASS = localhost_DATABASE_PASS
# DATABASE_CONNECTION_PREFIX = localhost_DATABASE_CONNECTION_PREFIX
# DATABASE_SERVER = localhost_DATABASE_SERVER
# DATABASE_SERVER_URI = localhost_DATABASE_SERVER_URI
# DATABASE_URI = localhost_DATABASE_URI

# if EXECUTION_ENVIRONMENT == 'pythonanywhere':
#     DATABASE_HOST_ADDRESS = pythonanywhere_ganimedes_DATABASE_HOST_ADDRESS
#     DATABASE_NAME = pythonanywhere_ganimedes_DATABASE_NAME
#     DATABASE_USER = pythonanywhere_ganimedes_DATABASE_USER
#     DATABASE_PASS = pythonanywhere_ganimedes_DATABASE_PASS
#     DATABASE_CONNECTION_PREFIX = pythonanywhere_ganimedes_DATABASE_CONNECTION_PREFIX
#     DATABASE_SERVER = pythonanywhere_ganimedes_DATABASE_SERVER
#     DATABASE_SERVER_URI = pythonanywhere_ganimedes_DATABASE_SERVER_URI
#     DATABASE_URI = pythonanywhere_ganimedes_DATABASE_URI
#     if DATABASE_SERVER == 'pythonanywhere-ifestionas':
#         DATABASE_HOST_ADDRESS = pythonanywhere_ifestionas_DATABASE_HOST_ADDRESS
#         DATABASE_NAME = pythonanywhere_ifestionas_DATABASE_NAME
#         DATABASE_USER = pythonanywhere_ifestionas_DATABASE_USER
#         DATABASE_PASS = pythonanywhere_ifestionas_DATABASE_PASS
#         DATABASE_CONNECTION_PREFIX = pythonanywhere_ifestionas_DATABASE_CONNECTION_PREFIX
#         DATABASE_SERVER = pythonanywhere_ifestionas_DATABASE_SERVER
#         DATABASE_SERVER_URI = pythonanywhere_ifestionas_DATABASE_SERVER_URI
#         DATABASE_URI = pythonanywhere_ifestionas_DATABASE_URI
#####################################################################################################
######################################################################################################
#####################################################################################################
DATABASE_HOST_ADDRESS = DATABASE_SERVER
#DATABASE_SERVER_URI = DATABASE_CONNECTION_PREFIX + DATABASE_USER + ':' + DATABASE_PASS + '@' + DATABASE_HOST_ADDRESS
#DATABASE_URI = DATABASE_SERVER_URI + '/' + DATABASE_NAME
DATABASE_SERVER_URI = '{}{}:{}@{}'.format(DATABASE_CONNECTION_PREFIX, DATABASE_USER, DATABASE_PASS, DATABASE_HOST_ADDRESS)
DATABASE_URI = '{}/{}'.format(DATABASE_SERVER_URI, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DATABASE_URI
#####################################################################################################
#####################################################################################################
#store in os.environ in order to be used in subsequent configuration
os.environ["EXECUTION_ENVIRONMENT"] = EXECUTION_ENVIRONMENT
os.environ["EXECUTION_MODE"] = EXECUTION_MODE
os.environ["SERVER"] = SERVER
os.environ["DATABASE_SERVER"] = DATABASE_SERVER
os.environ["DATABASE_NAME"] = DATABASE_NAME
os.environ["DATABASE_SERVER_URI"] = DATABASE_SERVER_URI
os.environ["DATABASE_URI"] = DATABASE_URI
os.environ["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
################################################################
log_config_param('EXECUTION_ENVIRONMENT', EXECUTION_ENVIRONMENT)
log_config_param('EXECUTION_MODE', EXECUTION_MODE)
log_config_param('SERVER', SERVER)
log_config_param('DATABASE_SERVER', DATABASE_SERVER)
log_config_param('DATABASE_NAME', DATABASE_NAME)
log_config_param('DATABASE_USER', DATABASE_USER)
log_config_param('DATABASE_PASS', DATABASE_PASS)
log_config_param('DATABASE_CONNECTION_PREFIX', DATABASE_CONNECTION_PREFIX)
log_config_param('DATABASE_HOST_ADDRESS', DATABASE_HOST_ADDRESS)
log_config_param('DATABASE_SERVER_URI', DATABASE_SERVER_URI)
log_config_param('DATABASE_URI', DATABASE_URI)
log_config_param('SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI)
################################################################

log_module_finish('database_configuration')

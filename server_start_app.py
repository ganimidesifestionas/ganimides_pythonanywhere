"""
This script runs the ganimides_website application using a development server.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#from server_debug_config import server_debug_config
#server_debug_config()
#from website_app.debug_services.debug_log_services import *
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import os.path
from os import environ
import configparser
print('### start: server_start_app')
thisfile = os.path.abspath(__file__)
thisDir = os.path.dirname(__file__)
exec_folder = os.path.abspath(os.path.dirname(__file__))
server_config_folder = os.path.dirname(exec_folder)
server_ini_filename = 'server.ini'
server_config_filename = 'server_config.py'
SERVER_INI_FILE = os.path.join(server_config_folder, server_ini_filename)
SERVER_CONFIG_FILE = os.path.join(server_config_folder, server_config_filename)
################################################################
print('...__file__', __file__)
print('...DirName', thisDir)
print('...exec_folder', exec_folder)
print('...server_config_folder', server_config_folder)
print('...SERVER_INI_FILE', SERVER_INI_FILE)
print('...SERVER_CONFIG_FILE', SERVER_CONFIG_FILE)
#print (os.path.isfile(SERVER_CONFIG_FILE))
print('...start-server.ini')
if SERVER_INI_FILE and os.path.isfile(SERVER_INI_FILE) and os.access(SERVER_INI_FILE, os.R_OK):
    print('......server_ini_file FOUND...', SERVER_INI_FILE)
    os.environ["SERVER_INI_FILE"] = SERVER_INI_FILE
    config = configparser.ConfigParser()
    config.read(SERVER_INI_FILE)
    i=0
    for section in config:
        i=i+1
        k=0
        for key in config[section]:
            k=k+1
            os.environ[key.upper()] = config[section][key]
            print('......config_param', key.upper(), config[section][key])
else:
    print('......warning: Either the file is missing or not readable', 'SERVER_INI_FILE =', SERVER_INI_FILE)
print('...finish-server.ini')

if SERVER_CONFIG_FILE and os.path.isfile(SERVER_CONFIG_FILE) and os.access(SERVER_CONFIG_FILE, os.R_OK):
    print('...server_config_file FOUND...', SERVER_CONFIG_FILE)
    os.environ["SERVER_CONFIG_FILE"] = SERVER_CONFIG_FILE
else:
    print('...warning: Either the file is missing or not readable', 'SERVER_CONFIG_FILE =', SERVER_CONFIG_FILE)

print('...start-import flask app from website_app')
from website_app import app
print('...finish-import flask app from website_app')
from database import init_database as init_application_database
from website_app.module_authorization.database import init_database as init_authorization_database
from website_app.module_administration.database import init_database as init_administration_database
print('...###INIT DATABASES START')
init_administration_database()
init_authorization_database()
init_application_database()
print('...###INIT DATABASES FINISH')
print('### finish: server_start_app')
if __name__ == '__main__':
    print('')
    print('### START APP')
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    debugOption = True
    msg = 'app.run(HOST={}, PORT={}, debug={})'.format(HOST, PORT, debugOption)
    print('### about to execute:', msg)
    msg = 'app started on [{}] port {} ...'.format(HOST, PORT)
    print('###', msg)
    print('')
    app.run(HOST, PORT, debug=False)
    print('')
    print('### APP FINISH')

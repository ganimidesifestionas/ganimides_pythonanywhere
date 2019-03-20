"""
This script runs the ganimides_website application using a development server.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import os.path
from os import environ
import configparser
from website_app.debug_services.debug_log_services import *
from server_debug_config import server_debug_config
server_debug_config()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
log_module_start('server_start_app')
thisfile = os.path.abspath(__file__)
thisDir = os.path.dirname(__file__)
exec_folder = os.path.abspath(os.path.dirname(__file__))
server_config_folder = os.path.dirname(exec_folder)
server_ini_filename = 'server.ini'
server_config_filename = 'server_config.py'
SERVER_INI_FILE = os.path.join(server_config_folder , server_ini_filename)
SERVER_CONFIG_FILE = os.path.join(server_config_folder , server_config_filename)
################################################################
log_variable('__file__', __file__)
log_variable('DirName', thisDir)
log_variable('exec_folder', exec_folder)
log_variable('server_config_folder', server_config_folder)
log_variable('SERVER_INI_FILE',SERVER_INI_FILE)
log_variable('SERVER_CONFIG_FILE',SERVER_CONFIG_FILE)
#print (os.path.isfile(SERVER_CONFIG_FILE))
log_start('server.ini')
if SERVER_INI_FILE and os.path.isfile(SERVER_INI_FILE) and os.access(SERVER_INI_FILE, os.R_OK):
    log_info('server_ini_file FOUND...', SERVER_INI_FILE)
    os.environ["SERVER_INI_FILE"] = SERVER_INI_FILE
    config = configparser.ConfigParser()
    config.read(SERVER_INI_FILE)
    for section in config:  
        for key in config[section]:  
            os.environ[key] = config[section][key]
            log_variable(key, config[section][key])
    # if 'DEFAULT' in config:
    #     for key in config['DEFAULT']:  
    #         os.environ[key] = config['DEFAULT'][key]
    #         log_variable(key, config['DEFAULT'][key])
else:
    log_warning("Either the file is missing or not readable",'SERVER_INI_FILE =', SERVER_INI_FILE)
log_finish('server.ini')

if SERVER_CONFIG_FILE and os.path.isfile(SERVER_CONFIG_FILE) and os.access(SERVER_CONFIG_FILE, os.R_OK):
    log_info('server_config_file FOUND...', SERVER_CONFIG_FILE)
    os.environ["SERVER_CONFIG_FILE"] = SERVER_CONFIG_FILE
else:
    log_warning("Either the file is missing or not readable",'SERVER_CONFIG_FILE =', SERVER_CONFIG_FILE)

#print('3')
log_start('import flask app from website_app')
from website_app import app
log_finish('import flask app from website_app')
#print(4)
from database import init_database as init_application_database
from website_app.module_authorization.database import init_database as init_authorization_database
from website_app.module_administration.database import init_database as init_administration_database
log_start('###INIT DATABASES START###')
init_administration_database()
init_authorization_database()
init_application_database()
log_finish('###INIT DATABASES START###')
log_module_finish('server_start_app')
if __name__ == '__main__':
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
    print('###',msg)
    app.run(HOST, PORT, debug=False)
    print('### APP FINISH')

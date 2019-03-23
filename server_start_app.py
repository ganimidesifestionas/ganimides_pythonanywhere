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
thisFileName = os.path.basename(__file__)
exec_folder = os.path.abspath(os.path.dirname(__file__))
server_config_folder = os.path.dirname(exec_folder)
server_ini_filename = 'server.ini'
server_config_filename = 'server_config.py'
server_ini_file = os.path.join(server_config_folder, server_ini_filename)
server_config_file = os.path.join(server_config_folder, server_config_filename)
server_relative_config_path = "..\\"
################################################################
# print('...Server_Startup_Program =', __file__)
# print('...Server_Startup_Folder =', thisDir)
# print('...Server_Startup_ProgramName =', thisFileName)
# print('...Server_Exec_Folder =', exec_folder)
# print('...Server_Config_Folder =', server_config_folder)
# print('...server_ini_file =', server_ini_file)
# print('...server_config_file =', server_config_file)
# print('...server_ini_file_name =', server_ini_filename)
# print('...server_config_file_name =', server_config_filename)
# print('...server_relative_config_path =', server_relative_config_path)
#print (os.path.isfile(server_config_file))
################################################################
ServerDictionary = {}
ServerDictionary.update({'Server_Startup_Program':__file__})
ServerDictionary.update({'Server_Startup_Folder':thisDir})
ServerDictionary.update({'Server_Startup_Program_Name':thisFileName})
ServerDictionary.update({'Server_Startup_Execfolder':exec_folder})
ServerDictionary.update({'Server_Config_Folder':server_config_folder})
ServerDictionary.update({'server_ini_file_Name':server_ini_filename})
ServerDictionary.update({'server_config_file_Name':server_config_filename})
ServerDictionary.update({'server_ini_file':server_ini_file})
ServerDictionary.update({'server_config_file':server_config_file})
ServerDictionary.update({'server_relative_config_path':server_relative_config_path})

for serveritem in ServerDictionary:
    os.environ[serveritem.upper()] = ServerDictionary.get(serveritem)
    print('...env param: '+serveritem.upper()+' =', os.environ.get(serveritem.upper()))
################################################################
print('...start-server.ini')
if server_ini_file and os.path.isfile(server_ini_file) and os.access(server_ini_file, os.R_OK):
    print('......server_ini_file FOUND...', server_ini_file)
    config = configparser.ConfigParser()
    config.read(server_ini_file)
    i = 0
    for section in config:
        i = i + 1
        k = 0
        print('......', i, 'server.ini section =', section)
        for key in config[section]:
            k = k + 1
            os.environ[key.upper()] = config[section][key].replace("'", "")
            print('.........', k, 'config_param', key.upper(), config[section][key])
else:
    print('......warning:', 'server_ini_file NOT-FOUND:[', server_ini_file, '] Either the file is missing or not readable')
print('...finish-server.ini')

#for debug: list all env params
# for envitem in os.environ:
#     print('...env param: '+envitem+' =', os.environ.get(envitem))

if server_config_file and os.path.isfile(server_config_file) and os.access(server_config_file, os.R_OK):
    print('...server_config_file FOUND...', server_config_file)
else:
    print('...warning:', 'server_config_file NOT-FOUND:[', server_config_file, '] Either the file is missing or not readable')

#exit(0)

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
    #debug=True autoreloads flask when a change has been detected
    app.run(HOST, PORT, debug=True)
    print('')
    print('### APP FINISH')

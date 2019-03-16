"""
This script runs the ganimides_website application using a development server.
"""
print('0')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import os.path
from os import environ
print('1')
from debug_services.debug_log_services import *
print('2')
#from server_debug_config import debug_config
#debug_config()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
log_module_start('runserver')
#log_info('######################################################')
#log_info('###RUN APP ON SERVER###')
#log_info('######################################################')
#log_info('### INIT START')
# # # # #
thisfile = os.path.abspath(__file__)
exec_folder = os.path.abspath(os.path.dirname(__file__))
server_config_folder = os.path.dirname(exec_folder)
server_config_filename = 'server_config.py'
server_config_file = os.path.join(server_config_folder , server_config_filename)
################################################################
# print('      ', '__file__ =',__file__)
# print('      ', 'exec_folder =', exec_folder)
# print('      ', 'server_config_folder =', server_config_folder)
# print('      ', 'server_config_file =', server_config_file)
# print (os.path.isfile(server_config_file))
if server_config_file and os.path.isfile(server_config_file) and os.access(server_config_file, os.R_OK):
    log_variable('server_config_file =', server_config_file)
    os.environ["SERVER_CONFIG_FILE"] = server_config_file
else:
    log_warning("Either the file is missing or not readable",'server_config_file =', server_config_file)

print('3')
from website_app import app
print(4)
from database import init_database as init_application_database
print(5)
from website_app.module_authorization.database import init_database as init_authorization_database
print(6)
from website_app.module_administration.database import init_database as init_administration_database
print(7)
log_info('### INIT DATABASES START')
init_administration_database()
init_authorization_database()
init_application_database()
#print('')
log_info('### INIT DATABASES FINISH')
log_info('### INIT END')
log_module_finish('runserver')

if __name__ == '__main__':
    print('### START APP')
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    debugOption = True
    msg = 'app.run(HOST={}, PORT={}, debug={})'.format(HOST, PORT, debugOption)
    print('###   ', msg)
    msg = 'app started on [{}] port {} ...'.format(HOST, PORT)
    print('###',msg)
    #log_info('###', msg)
    app.run(HOST, PORT, debug=False)
    print('### APP FINISH')

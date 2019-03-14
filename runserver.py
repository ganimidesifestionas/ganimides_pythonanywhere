"""
This script runs the ganimides_website application using a development server.
"""
print('0')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from os import environ
print('1')
from website_app.external_services.debug_log_services import *
print('2')
from server_debug_config import debug_config
print('3')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
debug_config()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
log_module_start('runserver')
#log_info('######################################################')
#log_info('###RUN APP ON SERVER###')
#log_info('######################################################')
log_info('### INIT START')
# # # # #
from website_app import app
from database import init_database as init_application_database
from website_app.module_authorization.database import init_database as init_authorization_database
from website_app.module_administration.database import init_database as init_administration_database

log_info('### INIT DATABASES START')
#init_administration_database()
#init_authorization_database()
#init_application_database()
#print('')
log_info('### INIT DATABASES FINISH')
log_info('### INIT END')
log_module_finish('runserver')

if __name__ == '__main__':
    log_info('### START APP')
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    debugOption = True
    msg = 'app.run(HOST={}, PORT={}, debug={})'.format(HOST, PORT, debugOption)
    log_info('###', msg)
    msg = 'app started on [{}] port {} ...'.format(HOST, PORT)
    log_info('###', msg)
    app.run(HOST, PORT, debug=False)
    log_info('### APP FINISH')

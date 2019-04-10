"""
This script runs the ganimides_website application.
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import os.path
from os import environ
import configparser
from colorama import init as colorsInit, Fore, Back, Style
from server_init import initialize_server

colorsInit()
print(Fore.WHITE+'### start: server_start_app')

initialize_server(startupProgram_fullpathfile=__file__, server_ini_filename='server.ini', debug=False, print_env_params=False, print_all_env_params=False)
print(Fore.WHITE+'   ###start: import flask app from website_app')
from website_app import app
print(Fore.WHITE+'   ###finish: import flask app from website_app')

print(Fore.WHITE+'   ###start: Init databases')
from database import init_database as init_application_database
from website_app.module_authorization.database import init_database as init_authorization_database
from website_app.module_administration.database import init_database as init_administration_database
# init_administration_database()
# init_authorization_database()
# init_application_database()
print(Fore.WHITE+'   ###finish: Init databases')
# print all config params
# if app.config.get('DEBUG_STARTUP'):
#     keylist = sorted(app.config.items())
#     for key in keylist:
#         print('   app-cfg-Key {}={}'.format(key[0], key[1]))

# print all env params
# if app.config.get('DEBUG_STARTUP'):
#     print('')
#     for envitem in os.environ:
#         print('   env param {}={}'.format(envitem, os.environ.get(envitem)))

# exit(0)

print('### finish: server_start_app')
if __name__ == '__main__':
    print(Fore.WHITE+'')
    print('### START APP')

    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    print('   SERVER_HOST set to {} (from app.config)'.format(HOST))
    print('   SERVER_PORT set to {} (from app.config)'.format(PORT))

    debugOption = True
    use_reloaderOption = False
    if app.config.get('USE_RELOADER'):
        print('   USE_RELOADER option set ON (from app.config)')
        use_reloaderOption = True
    else:
        print('   USE_RELOADER option set OFF (from app.config)')
        use_reloaderOption = False
    if app.config.get('FLASK_DEBUG'):
        print('   DEBUG option set OFF (from app.config)')
        debugOption = False
    else:
        print('   DEBUG option set ON  (from app.config)')
        debugOption = True
    print('FLASK_DEBUG', app.config.get('FLASK_DEBUG'))
    print('DEBUG', app.config.get('DEBUG'))
    debugOption = True
    
    msg = 'app.run(HOST={}, PORT={}, debug={},use_reloader={})'.format(HOST, PORT, debugOption, use_reloaderOption)
    print('### about to execute:', msg)

    msg = 'app started on [{}] port {} ...'.format(HOST, PORT)
    print('###', msg)
    print('')
    # debug=True autoreloads flask when a change has been detected
    # use_reloaderOption=False avoid compiling twice
    app.run(HOST, PORT, debug=debugOption, use_reloader=use_reloaderOption)
    print('')
    print('### APP FINISH')

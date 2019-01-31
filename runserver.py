"""
This script runs the ganimides_website application using a development server.
"""
# # # # # #
print(__name__, '######################################################')
print(__name__, '###RUN APP ON SERVER###')
print(__name__, '######################################################')
print(__name__, '### INIT START----------------------------------------')
# # # # #
from os import environ
from website_app import app
from database import init_database as init_application_database
from website_app.module_authorization.database import init_database as init_authorization_database
from website_app.module_administration.database import init_database as init_administration_database

print(__name__, '### INIT DATABASES START--------------------------------')
init_administration_database()
init_authorization_database()
init_application_database()
print(__name__, '### INIT DATABASES FINISH-------------------------------')
print(__name__, '### INIT END--------------------------------------------')

if __name__ == '__main__':
    print(__name__, '### START APP(flask)------------------------------------')
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    print(__name__, '   app.run','host =', HOST, 'port =', PORT)
    app.run(HOST, PORT, debug=False)
    print(__name__, '### APP FINISH-----------------------------------------')

# myServer/instance/config.py

import os
DISPLAY_CONFIGURATION = False
APPLICATION_BASEFOLDER = os.environ["APPLICATION_BASEFOLDER"]
config_file = os.path.abspath(__file__)
config_filename = os.path.basename(__file__)
config_path = os.path.abspath(os.path.dirname(__file__))
config_base_folder = os.path.dirname(config_path)
config_folder = config_file.replace(config_filename, '').replace(APPLICATION_BASEFOLDER, '')
################################################################
print('      ', '__file__ =',__file__)
print('      ', 'config_file =', config_file)
print('      ', 'config_path =', config_path)
print('      ', 'config_folfer =', config_folder)
print('      ', 'config_filename =', config_filename)
print('      ', 'config_base_folder =', config_base_folder)
#####################################################################
INSTANCE_CONFIG_FILE = config_file
INSTANCE_CONFIG_PATH = config_path
INSTANCE_CONFIG_BASE_FOLDER = config_base_folder
INSTANCE_CONFIG_FOLDER = config_folder
INSTANCE_CONFIG_FILENAME = config_filename
#####################################################################
#from the server config
EXECUTION_ENVIRONMENT = os.environ.get('EXECUTION_ENVIRONMENT', 'localhost')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SERVER = os.environ.get('SERVER')

EYECATCH = 'INSTANCE'
EXECUTION_MODE = 'sandbox'
MAIL_SERVER_PROVIDER = 'google' #'mailjet' #'yandex'

################################################################
### Secret key for signing cookies
################################################################
SECRET_KEY = 'server-instance-aeiotheosomegasgeometreip9Bv<3Eid9%$i01'
SECURITY_PASSWORD_SALT = 'server-instance-aeiotheosomegasgeometreip9Bvtispaolas'

#############################################################################################
### mail accounts
#############################################################################################
MAIL_SENDER = 'noreply@ganimides.com>'
MAIL_SUBJECT_PREFIX = '[ganimides]'
MAIL_DEFAULT_SENDER = 'noreply@ganimides.com'
MAIL_ADMIN_SENDER = 'admin@ganimides.com'
MAIL_SUPPORT_SENDER = 'support@ganimides.com'
WEBSITE_ADMIN = os.environ.get('WEBSITE_ADMIN', 'admin@ganimides.com')

################################################################
### database config
################################################################
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = True

################################################################
### miscellaneous
################################################################
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SSL_REDIRECT = False
# Application threads. A common general assumption is using 2 per available processor cores - to handle incoming requests using one and performing background operations using the other.
THREADS_PER_PAGE = 2
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True
# Use a secure, unique and absolutely secret key for signing the data.
CSRF_SESSION_KEY = "aeiotheosomegasgeometrei"

#############################################################################################
# mail server
#############################################################################################
if MAIL_SERVER_PROVIDER == 'mailjet':
    MAIL_SERVER = os.environ.get('mailjet_MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('mailjet_MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('mailjet_MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USE_SSL = os.environ.get('mailjet_MAIL_USE_SSL', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('mailjet_MAIL_USERNAME', '...@gmail.com')
    MAIL_PASSWORD = os.environ.get('mailjet_MAIL_PASSWORD', '****')
    MAIL_APIKEY_PUBLIC = os.environ.get('mailjet_MAIL_APIKEY_PUBLIC','...')
    MAIL_APIKEY_PRIVATE = os.environ.get('mailjet_MAIL_APIKEY_PRIVATE','...')
else:
    if MAIL_SERVER_PROVIDER == 'yandex':
        MAIL_SERVER = os.environ.get('yandex_MAIL_SERVER', 'smtp.googlemail.com')
        MAIL_PORT = int(os.environ.get('yandex_MAIL_PORT', '587'))
        MAIL_USE_TLS = os.environ.get('yandex_MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
        MAIL_USE_SSL = os.environ.get('yandex_MAIL_USE_SSL', 'true').lower() in ['true', 'on', '1']
        MAIL_USERNAME = os.environ.get('yandex_MAIL_USERNAME', '...@gmail.com')
        MAIL_PASSWORD = os.environ.get('yandex_MAIL_PASSWORD', '****')
        MAIL_APIKEY_PUBLIC = os.environ.get('yandex_MAIL_APIKEY_PUBLIC','...')
        MAIL_APIKEY_PRIVATE = os.environ.get('yandex_MAIL_APIKEY_PRIVATE','...')
    else:
        MAIL_SERVER = os.environ.get('google_MAIL_SERVER', 'smtp.googlemail.com')
        MAIL_PORT = int(os.environ.get('google_MAIL_PORT', '587'))
        MAIL_USE_TLS = os.environ.get('google_MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
        MAIL_USE_SSL = os.environ.get('google_MAIL_USE_SSL', 'true').lower() in ['true', 'on', '1']
        MAIL_USERNAME = os.environ.get('google_MAIL_USERNAME', '...@gmail.com')
        MAIL_PASSWORD = os.environ.get('google_MAIL_PASSWORD', '****')
        MAIL_APIKEY_PUBLIC = os.environ.get('google_MAIL_APIKEY_PUBLIC','...')
        MAIL_APIKEY_PRIVATE = os.environ.get('google_MAIL_APIKEY_PRIVATE','...')

################################################################
### Recaptcha
################################################################
RECAPTCHA_SITE_KEY = os.environ.get('localhost_google_RECAPTCHA_SITE_KEY','...')
RECAPTCHA_SECRET_KEY = os.environ.get('localhost_google_RECAPTCHA_SECRET_KEY','...')
RECAPTCHA_INVISIBLE_SITE_KEY = os.environ.get('localhost_google_RECAPTCHA_INVISIBLE_SITE_KEY','...')
RECAPTCHA_INVISIBLE_SECRET_KEY = os.environ.get('localhost_google_RECAPTCHA_INVISIBLE_SECRET_KEY','...')
GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get('localhost_google_RECAPTCHA_SITE_KEY','...')
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('localhost_google_RECAPTCHA_SECRET_KEY','...')
GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY = os.environ.get('localhost_google_RECAPTCHA_INVISIBLE_SITE_KEY','...')
GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY = os.environ.get('localhost_google_RECAPTCHA_INVISIBLE_SECRET_KEY','...')
if EXECUTION_ENVIRONMENT=='pythonanywhere':
    RECAPTCHA_SITE_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_SITE_KEY','...')
    RECAPTCHA_SECRET_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_SECRET_KEY','...')
    RECAPTCHA_INVISIBLE_SITE_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_INVISIBLE_SITE_KEY','...')
    RECAPTCHA_INVISIBLE_SECRET_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_INVISIBLE_SECRET_KEY','...')
    GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_SITE_KEY','...')
    GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_SECRET_KEY','...')
    GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_INVISIBLE_SITE_KEY','...')
    GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY = os.environ.get('pythonanywhere_google_RECAPTCHA_INVISIBLE_SECRET_KEY','...')

################################################################
### ipstack access key
################################################################
IPSTACK_API_ACCESSKEY = '4022cfd2249c3431953ecf599152892e'
IPSTACK_URL = 'http://api.ipstack.com/'
IPSTACK_URL_CMD = 'http://api.ipstack.com/{0}?access_key={1}'
# ################################################################
# ### print
# ################################################################
if DISPLAY_CONFIGURATION :
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### BASE_DIR =', BASE_DIR)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### SERVER =', SERVER)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### EXECUTION_ENVIRONMENT =', EXECUTION_ENVIRONMENT)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### EXECUTION_MODE =', EXECUTION_MODE)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '--------------------------------------------------')
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### SQLALCHEMY_DATABASE_URI =',SQLALCHEMY_DATABASE_URI)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '--------------------------------------------------')
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_SERVER_PROVIDER =',MAIL_SERVER_PROVIDER)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_SERVER =',MAIL_SERVER)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_PORT =',MAIL_PORT)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_USE_TLS =',MAIL_USE_TLS)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_USE_SSL =',MAIL_USE_SSL)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_USERNAME =',MAIL_USERNAME)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_PASSWORD =',MAIL_PASSWORD)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_APIKEY_PUBLIC =',MAIL_APIKEY_PUBLIC)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_APIKEY_PRIVATE =',MAIL_APIKEY_PRIVATE)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '--------------------------------------------------')
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### GOOGLE_RECAPTCHA_SITE_KEY =',GOOGLE_RECAPTCHA_SITE_KEY)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### GOOGLE_RECAPTCHA_SECRET_KEY =',GOOGLE_RECAPTCHA_SECRET_KEY)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY =',GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY =',GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '--------------------------------------------------')
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### SECRET_KEY =',SECRET_KEY)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### SECURITY_PASSWORD_SALT =',SECURITY_PASSWORD_SALT)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '--------------------------------------------------')
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_SENDER =',MAIL_SENDER)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_SUBJECT_PREFIX =',MAIL_SUBJECT_PREFIX)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_DEFAULT_SENDER =',MAIL_DEFAULT_SENDER)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_ADMIN_SENDER =',MAIL_ADMIN_SENDER)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### MAIL_SUPPORT_SENDER =',MAIL_SUPPORT_SENDER)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '### WEBSITE_ADMIN =',WEBSITE_ADMIN)
    print('      ', INSTANCE_CONFIG_FOLDER, INSTANCE_CONFIG_FILENAME, EYECATCH, '--------------------------------------------------')

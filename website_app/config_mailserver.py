# mailserver_config.py
import os
from website_app.debug_services.debug_log_services import *

log_module_start('mailserver_configuration')

MAIL_SERVER_PROVIDER = os.environ.get('MAIL_SERVER_PROVIDER', 'GOOGLE')
log_variable('MAIL_SERVER_PROVIDER', MAIL_SERVER_PROVIDER)

################################################################
### mail servers
################################################################
MAILJET_MAIL_SERVER = 'in-v3.mailjet.com'
MAILJET_MAIL_PORT = '587' # Port 25 or 587 (some providers block port 25). If TLS on port 587 doesn't work, try using port 465 and/or using SSL instead
MAILJET_MAIL_USE_TLS = 'True'
MAILJET_MAIL_USE_SSL = 'True'
MAILJET_MAIL_USERNAME = 'f8d33207c3c7a1ecaf2f74e809b57786'
MAILJET_MAIL_PASSWORD = '2d6a3c2de41ff45b5435382f3e267580'
MAILJET_MAIL_APIKEY_PUBLIC ='f8d33207c3c7a1ecaf2f74e809b57786'
MAILJET_MAIL_APIKEY_PRIVATE ='2d6a3c2de41ff45b5435382f3e267580'

YANDEX_MAIL_SERVER = "smtp.yandex.ru"
YANDEX_MAIL_PORT = '587'
YANDEX_MAIL_USE_TLS = 'True'
YANDEX_MAIL_USE_SSL = 'True'
YANDEX_MAIL_USERNAME = '...' #without the @yandex.ru
YANDEX_MAIL_PASSWORD = '***'
YANDEX_MAIL_APIKEY_PUBLIC = '...'
YANDEX_MAIL_APIKEY_PRIVATE = '...'

GOOGLE_MAIL_SERVER = "smtp.gmail.com"
GOOGLE_MAIL_PORT = '587'
GOOGLE_MAIL_USE_TLS = 'False'
GOOGLE_MAIL_USE_SSL = 'True'
GOOGLE_MAIL_USERNAME = 'akamas2020@gmail.com'
GOOGLE_MAIL_PASSWORD = 'philea13'
GOOGLE_MAIL_USERNAME = 'bstarr131@gmail.com'
GOOGLE_MAIL_PASSWORD = 'bstarr13'
GOOGLE_MAIL_USERNAME = 'spithas@leandrou.com'
GOOGLE_MAIL_PASSWORD = 'spithas3116'
GOOGLE_MAIL_APIKEY_PUBLIC = '...'
GOOGLE_MAIL_APIKEY_PRIVATE = '...'

if MAIL_SERVER_PROVIDER == 'MAILJET':
    MAIL_SERVER = MAILJET_MAIL_SERVER
    MAIL_PORT = MAILJET_MAIL_PORT
    MAIL_USE_TLS = MAILJET_MAIL_USE_TLS
    MAIL_USE_SSL = MAILJET_MAIL_USE_SSL
    MAIL_USERNAME = MAILJET_MAIL_USERNAME
    MAIL_PASSWORD = MAILJET_MAIL_PASSWORD
    MAIL_APIKEY_PUBLIC = MAILJET_MAIL_APIKEY_PUBLIC
    MAIL_APIKEY_PRIVATE = MAILJET_MAIL_APIKEY_PRIVATE
else:
    if MAIL_SERVER_PROVIDER == 'YANDEX':
        MAIL_SERVER = YANDEX_MAIL_SERVER
        MAIL_PORT = YANDEX_MAIL_PORT
        MAIL_USE_TLS = YANDEX_MAIL_USE_TLS
        MAIL_USE_SSL = YANDEX_MAIL_USE_SSL
        MAIL_USERNAME = YANDEX_MAIL_USERNAME
        MAIL_PASSWORD = YANDEX_MAIL_PASSWORD
        MAIL_APIKEY_PUBLIC = YANDEX_MAIL_APIKEY_PUBLIC
        MAIL_APIKEY_PRIVATE = YANDEX_MAIL_APIKEY_PRIVATE
    else:
        MAIL_SERVER = GOOGLE_MAIL_SERVER
        MAIL_PORT = GOOGLE_MAIL_PORT
        MAIL_USE_TLS = GOOGLE_MAIL_USE_TLS
        MAIL_USE_SSL = GOOGLE_MAIL_USE_SSL
        MAIL_USERNAME = GOOGLE_MAIL_USERNAME
        MAIL_PASSWORD = GOOGLE_MAIL_PASSWORD
        MAIL_APIKEY_PUBLIC = GOOGLE_MAIL_APIKEY_PUBLIC
        MAIL_APIKEY_PRIVATE = GOOGLE_MAIL_APIKEY_PRIVATE

################################################################
log_config_param('MAIL_SERVER', MAIL_SERVER)
log_config_param('MAIL_PORT', MAIL_PORT)
log_config_param('MAIL_USE_TLS', MAIL_USE_TLS)
log_config_param('MAIL_USE_SSL', MAIL_USE_SSL)
log_config_param('MAIL_USERNAME', MAIL_USERNAME)
log_config_param('MAIL_PASSWORD', MAIL_PASSWORD)
log_config_param('MAIL_APIKEY_PUBLIC', MAIL_APIKEY_PUBLIC)
log_config_param('MAIL_APIKEY_PRIVATE', MAIL_APIKEY_PRIVATE)
################################################################

log_module_finish('mailserver_configuration')

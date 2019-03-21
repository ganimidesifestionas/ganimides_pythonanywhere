"""Google configurations google_config.py"""
import os
from website_app.debug_services.debug_log_services import *
#import .debug_services.debug_log_services
#.debug_log_services import *

#class Config(object):
log_module_start('google_configuration')
EYECATCH = 'GOOGLE'

#google maps
GOOGLE_MAPS_API_KEY = 'AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY'

#google mail server
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


#google recapcha
localhost_GOOGLE_RECAPTCHA_SITE_KEY = "6LcD3XkUAAAAABAoO2p4WOoBGg6uRyCoVCcGNCFV"
localhost_GOOGLE_RECAPTCHA_SECRET_KEY = "6LcD3XkUAAAAAHTNpV8RsDN8CybCNEJ0htRddCMq"
localhost_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY = "6LfL2HkUAAAAAF8ot-2aPAHYzHPAAxvLtKI-PyXi"
localhost_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY = "6LfL2HkUAAAAAIdjgyCwgSaV2hvOS6APpoXot1yw"

pythonanywhere_GOOGLE_RECAPTCHA_SITE_KEY = "6LeQxnwUAAAAAAyscnSdBS0RbNo6BEDje-trtOV-"
pythonanywhere_GOOGLE_RECAPTCHA_SECRET_KEY = "6LeQxnwUAAAAAGjxVdpUGhRREi5xQQQhRfROJCmZ"
pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY = "...."
pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY = "..."

EXECUTION_ENVIRONMENT = os.environ.get('EXECUTION_ENVIRONMENT').replace("'", '')
if not EXECUTION_ENVIRONMENT:
    EXECUTION_ENVIRONMENT = 'localhost'
EXECUTION_MODE = os.environ.get('EXECUTION_MODE').replace("'", '')
if not EXECUTION_MODE:
    EXECUTION_MODE = 'design'

#default is localhost
GOOGLE_RECAPTCHA_PUBLIC_KEY = localhost_GOOGLE_RECAPTCHA_SITE_KEY
GOOGLE_RECAPTCHA_PRIVATE_KEY = localhost_GOOGLE_RECAPTCHA_SECRET_KEY
if EXECUTION_ENVIRONMENT == 'pythonanywhere':
    GOOGLE_RECAPTCHA_PUBLIC_KEY = pythonanywhere_GOOGLE_RECAPTCHA_SITE_KEY
    GOOGLE_RECAPTCHA_PRIVATE_KEY = pythonanywhere_GOOGLE_RECAPTCHA_SECRET_KEY

# store in env for later in flask config
RECAPTCHA_PUBLIC_KEY = GOOGLE_RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = GOOGLE_RECAPTCHA_PRIVATE_KEY
os.environ['RECAPTCHA_PUBLIC_KEY'] = GOOGLE_RECAPTCHA_PUBLIC_KEY
os.environ['RECAPTCHA_PRIVATE_KEY'] = GOOGLE_RECAPTCHA_PRIVATE_KEY

log_config_param('localhost_GOOGLE_RECAPTCHA_SITE_KEY', localhost_GOOGLE_RECAPTCHA_SITE_KEY)
log_config_param('localhost_GOOGLE_RECAPTCHA_SECRET_KEY', localhost_GOOGLE_RECAPTCHA_SECRET_KEY)
log_config_param('localhost_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY', localhost_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY)
log_config_param('localhost_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY', localhost_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY)

log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_SITE_KEY', pythonanywhere_GOOGLE_RECAPTCHA_SITE_KEY)
log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_SECRET_KEY', pythonanywhere_GOOGLE_RECAPTCHA_SECRET_KEY)
log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY', pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY)
log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY', pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY)

log_config_param('EXECUTION_ENVIRONMENT', EXECUTION_ENVIRONMENT)
log_config_param('RECAPTCHA_PUBLIC_KEY', GOOGLE_RECAPTCHA_PUBLIC_KEY)
log_config_param('RECAPTCHA_PRIVATE_KEY', GOOGLE_RECAPTCHA_PRIVATE_KEY)

log_module_finish('google_configuration')

# class GoogleConfig() #Config):
#     log_module_start('google_configuration')
#     EYECATCH = 'GOOGLE'
#     print('localhost_GOOGLE_RECAPTCHA_SITE_KEY', Config.localhost_GOOGLE_RECAPTCHA_SITE_KEY)
#     log_config_param('localhost_GOOGLE_RECAPTCHA_SITE_KEY', Config.localhost_GOOGLE_RECAPTCHA_SITE_KEY)
#     # log_config_param('localhost_GOOGLE_RECAPTCHA_SECRET_KEY', localhost_GOOGLE_RECAPTCHA_SECRET_KEY)
#     # log_config_param('localhost_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY', localhost_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY)
#     # log_config_param('localhost_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY', localhost_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY)

#     # log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_SITE_KEY', pythonanywhere_GOOGLE_RECAPTCHA_SITE_KEY)
#     # log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_SECRET_KEY', pythonanywhere_GOOGLE_RECAPTCHA_SECRET_KEY)
#     # log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY', pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY)
#     # log_config_param('pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY', pythonanywhere_GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY)
#     log_module_finish('google_configuration')

#####################################################
# config = {
#     'google' : GoogleConfig
# }
#####################################################
if __name__ == '__main__':
    print('google_configuration:')
    #print('google_configuration:', active_module, active_component_debug_enabled, active_component_debug_level)

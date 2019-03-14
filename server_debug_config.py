"""
This script configures the debug_log_services
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from os import environ
from website_app.external_services.debug_log_services import *
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def debug_config():
    set_debug_off('@app.after_request')
    set_debug_off('@app.before_request')
    set_debug_off('#@authorization.before_request')
    set_debug_off('@authorization.after_request')
    set_debug_off('log_services')
    set_debug_off('geolocation_services')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    set_log_suffix_timestamp(0)
    #set_log_suffix(__name__,'')
    set_debug_off('@app.*')
    set_debug_off('@authorization.*')

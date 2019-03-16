"""
This script configures the debug_log_services
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from os import environ
from debug_services.debug_log_services import *
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def debug_config():
    set_global_debug('ON')
    set_debug_defaults(onoff='ON', debuglevel=9)
    set_debug_level(module='webapp', debugOnOff='ON', debugLevel=9)
    set_debug_level(module='external_services', debugOnOff='ON', debugLevel=9)
    set_debug_level(module='*', component='geolocation_services', priority=88, debugOnOff='ON', debugLevel=9)
    set_debug_level(module='*', component='*', component_type='view' , priority=89, debugOnOff='ON', debugLevel=9)
    set_debug_level(module='*', component='log_services', priority=88, debugOnOff='ON', debugLevel=9)
    set_debug_level(component_type='request' , priority=89, debugOnOff='ON', debugLevel=9)
    set_debug_level(component_type='module' , priority=89, debugOnOff='ON', debugLevel=9)
    set_debug_level(component_type='function' , priority=89, debugOnOff='ON', debugLevel=9)

    # set_debug_off('@app.after_request')
    # set_debug_off('@app.before_request')
    # set_debug_off('#@authorization.before_request')
    # set_debug_off('@authorization.after_request')
    # set_debug_level('fillin_profile_forms', 1)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    set_log_suffix_timestamp(0)
    #set_log_suffix(__name__,'')
    #set_debug_off('@app.*')
    #set_debug_off('@authorization.*')

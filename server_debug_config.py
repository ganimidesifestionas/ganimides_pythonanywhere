"""
This script configures the debug_log_services at the server level
"""
from website_app.debug_services.debug_log_services import *
def server_debug_config():
    set_debug_defaults(onoff='ON', debuglevel=9)
    set_global_debug('OFF')
    set_debug_level(module='website_app', debugOnOff='ON', debugLevel=9)
    set_debug_level(module='debug_services', debugOnOff='ON', debugLevel=9)
    # set_debug_level(module='module_authorization', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='module_administration', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='external_services', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='*', component='geolocation_services', priority=88, debugOnOff='ON', debugLevel=9)
    # set_debug_level(module='*', component='log_services', priority=88, debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='*', component='*', component_type='view' , priority=89, debugOnOff='OFF', debugLevel=9)
    # set_debug_level(component_type='request' , priority=89, debugOnOff='OFF', debugLevel=9)
    # set_debug_level(component_type='module' , priority=89, debugOnOff='OFF', debugLevel=9)
    # set_debug_level(component_type='function' , priority=89, debugOnOff='OFF', debugLevel=9)
    # set_debug_off('@app.after_request')
    # set_debug_off('@app.before_request')
    # set_debug_off('#@authorization.before_request')
    # set_debug_off('@authorization.after_request')
    # set_debug_level('fillin_profile_forms', 1)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    set_log_suffix_timestamp('OFF')
    #set_log_suffix(__name__,'')
    #set_debug_off('@app.*')
    #set_debug_off('@authorization.*')

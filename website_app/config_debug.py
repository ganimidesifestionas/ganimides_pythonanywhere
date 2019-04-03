"""
This script configures the debug_log_services
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from os import environ
from website_app.debug_services.debug_log_services import *
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def debug_config_on_startup():
    log_start('debug_config_on_startup')
    config_from_environment_variables()    
    if os.environ.get('GLOBAL_DEBUG').upper() in ('OFF', '0', 'FALSE'):
        set_global_debug('OFF')
    else:
        set_global_debug('ON')
    set_debug_defaults(onoff='ON', debuglevel=9)
    set_debug_log_services_level('WARNING')  # WARNING , ERROR, INFO, BEGIN-END VARIABLE PARAMETER URL
    log_finish('debug_config_on_startup')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def debug_config():
    if os.environ.get('GLOBAL_DEBUG').upper() in ('OFF', '0', 'FALSE'):
        set_global_debug('OFF')
    else:
        set_global_debug('ON')
    set_global_debug('ON')
    log_start('debug_config')
    config_from_environment_variables()    
    set_debug_log_services_level('WARNING')  # WARNING , ERROR, INFO, BEGIN-END VARIABLE PARAMETER URL
    set_debug_defaults(onoff='OFF', debuglevel=9)
    #set_debug_level(component_type='include', priority=89, debugOnOff='ON', debugLevel=9)
    set_debug_level(component='visitspage', priority=88, debugOnOff='ON', debugLevel=9)

    # set_debug_level(module='website_app', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='module_authorization', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='module_administration', debugOnOff='OFF', debugLevel=9)
    #set_debug_level(module='debug_services', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='external_services', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='*', component='geolocation_services', priority=88, debugOnOff='OFF', debugLevel=9)
    #set_debug_level(module='*', component='log_services', priority=88, debugOnOff='ON', debugLevel=9)
    #set_debug_level(module='*', component='*', component_type='view', priority=89, debugOnOff='ON', debugLevel=9)
    #set_debug_level(component_type='request', priority=89, debugOnOff='ON', debugLevel=9)
    #set_debug_level(component_type='module', priority=89, debugOnOff='ON', debugLevel=9)
    # set_debug_level(component_type='function' , priority=89, debugOnOff='OFF', debugLevel=9)
    #set_debug_level(component='is_human', priority=89, debugOnOff='ON', debugLevel=9)

    # set_debug_off('@app.after_request')
    # set_debug_off('@app.before_request')
    # set_debug_off('#@authorization.before_request')
    # set_debug_off('@authorization.after_request')
    # set_debug_level('fillin_profile_forms', 1)
    log_finish('debug_config')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# if __name__ == '__main__':
#     #testing
#     debug_config()
#     active_module = 'a.external_services.geolocation_services'
#     retrieve_activecomponent_debug_info()
#     print('result:', active_module, active_component_debug_enabled, active_component_debug_level)
#     #set_log_suffix_timestamp(0)
#     #set_log_suffix(__name__,'')
#     #set_debug_off('@app.*')
#     #set_debug_off('@authorization.*')

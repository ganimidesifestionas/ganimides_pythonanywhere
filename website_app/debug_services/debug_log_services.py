import os
import sys
import re
import inspect
from datetime import datetime
global_debug_OFF = False
global_debug_enabled = True
debug_log_services_level = 'WARNING;ERROR;IMPORTANT'
default_debug_onoff = True
default_debug_level = 9
module_trace_enabled = True
message_compressed_enabled = False

max_line_length = 160
max_message_length = 120
max_module_trace_length = 60
message_display_mode = 'FIX-MESSAGE'  #'FIX-MODULE' #'FIX-MESSAGE' #'FIX-LINE' #'FLOAT'
message_prefix = ''
system_message_prefix = ''
debug_log_services_eyecatch = '[]'
level = 0
offset = ''
trailer = ''
Components = []
ConfigurationItems = {}
ModulesDictionary = {}
components_stack = {}
modules_NoDebug = {}
modules_Debug_Level = {}
moduleTypes_Debug = {}
modules_Debug = {}
offset_char = '.'
offset_tab = 3
sessionID = ''
UserID = ''
prefix = ''
suffix = ''
prefix_timestamp = False
suffix_timestamp = False
caller = ''
thisModule = ''
last_active_module = '?'
active_folder = ''
active_module = ''
active_component = ''
active_component_type = ''
active_component_debug_enabled = False
active_component_debug_level = 9
##########################################
def log_info(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 0) or debug_log_services_level.find('INFO') >= 0:
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_warning(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        # retrieve_activecomponent_debug_info()
        # if active_component_debug_enabled and active_component_debug_level > 1:
        if (active_component_debug_enabled and active_component_debug_level > 1) \
            or debug_log_services_level.find('WARNING') >= 0 \
            or debug_log_services_level.find('INFO') >= 0:
            msg = 'WARNING:{}'.format(msg)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_error(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        msg = 'ERROR:{}'.format(msg)
        message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
        print(message)
##########################################
def log_system_message(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    global system_message_prefix

    #if global_debug_enabled:
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
        # retrieve_activecomponent_debug_info()
        # if active_component_debug_enabled and active_component_debug_level > 1:
        #if (active_component_debug_enabled and active_component_debug_level > 1) \
        #    or debug_log_services_level.find('WARNING') >= 0 \
        #    or debug_log_services_level.find('INFO') >= 0:
    msg = '{}system-message:{}'.format(system_message_prefix, msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
    print(message)
##########################################
def log_system_info(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    global system_message_prefix
    #if global_debug_enabled:
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
        # retrieve_activecomponent_debug_info()
        # if active_component_debug_enabled and active_component_debug_level > 1:
        #if (active_component_debug_enabled and active_component_debug_level > 1) \
        #    or debug_log_services_level.find('WARNING') >= 0 \
        #    or debug_log_services_level.find('INFO') >= 0:
    msg = '{}system-info:{}'.format(system_message_prefix, msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
    print(message)
##########################################
def log_system_warning(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    #if global_debug_enabled:
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
        # retrieve_activecomponent_debug_info()
        # if active_component_debug_enabled and active_component_debug_level > 1:
        #if (active_component_debug_enabled and active_component_debug_level > 1) \
        #    or debug_log_services_level.find('WARNING') >= 0 \
        #    or debug_log_services_level.find('INFO') >= 0:
    msg = 'SYSTEM-WARNING:{}'.format(msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
    print(message)
##########################################
def log_variable(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('VARIABLE')>=0:
            msg = '{0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_env_param(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('VARIABLE')>=0:
            msg = 'env_param: {0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_file(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) \
            or debug_log_services_level.find('VARIABLE') >=0 \
            or debug_log_services_level.find('FILE') >=0 \
            :
            msg = 'file-{0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_variable_short(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('VARIABLE')>=0:
            valueStr = str(value)
            if len(valueStr)>37:
                valueStr = valueStr[0:37] + '...' 
            msg = '{0}={1}'.format(name, valueStr)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_param(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('PARAM')>=0:
            msg = 'param: {0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_config_param(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 3) or debug_log_services_level.find('CONFIG') >= 0:
            msg = 'config_param: {0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_important(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        # retrieve_activecomponent_debug_info()
        # if active_component_debug_enabled and active_component_debug_level > 1:
        if (active_component_debug_enabled and active_component_debug_level > 1) \
            or debug_log_services_level.find('IMPORTANT') >= 0 \
            or debug_log_services_level.find('WARNING') >= 0 \
            or debug_log_services_level.find('INFO') >= 0:
            msg = 'WARNING:{}'.format(msg)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            print(message)
##########################################
def log_url_param(name='', value=''):
    global offset
    global trailer
    global active_module
    global caller
    global debug_log_services_level
    if global_debug_enabled:
        caller = sys._getframe(1)  # Obtain calling frame
        active_module = caller.f_globals['__name__']
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('URL')>=0:
            msg = 'url-param {0}={1}'.format(name, value)
            message = formatted_message(msg=msg)
            print(message)
##########################################
def log_start(component_name='', component_type=''):
    global active_module
    global active_component
    global active_component_type
    global offset
    global level
    global components_stack
    global trailer
    global caller
    global thisModule
    global active_component_debug_enabled
    global active_component_debug_level
    global debug_log_services_level
    if global_debug_enabled:
        active_component = component_name
        active_component_type = component_type
        xcaller = sys._getframe(1)  # Obtain calling frame
        xactive_moduleX = xcaller.f_globals['__name__']
        if thisModule != xactive_moduleX:
            caller = xcaller
            active_module = xactive_moduleX

        retrieve_activecomponent_debug_info(active_module, active_component, active_component_type)
        if (active_component_debug_enabled and active_component_debug_level > 0) or debug_log_services_level.find('BEGIN-END')>=0:
            if active_component_type:
                ctype = active_component_type + '-'
            else:
                ctype = ''
            msg = '{}start [{}] from'.format(ctype, component_name)
            message = formatted_message(msg=msg)
            print(message)

        level = level + 1
        components_stack.update({level : [active_component, active_module, active_component_type]})
        offset = set_offset(level)
##########################################
def log_finish(component_name='', component_type=''):
    global offset
    global level
    global components_stack
    global trailer
    global active_component
    global active_component_type
    global active_module
    global caller
    global thisModule
    global active_component_debug_enabled
    global active_component_debug_level
    global debug_log_services_level
    if global_debug_enabled:
        xcaller = sys._getframe(1)  # Obtain calling frame
        xactive_moduleX = xcaller.f_globals['__name__']
        if thisModule != xactive_moduleX:
            caller = xcaller
            active_module = xactive_moduleX

        last_lev = -1
        last_component = '?'
        last_module = '?'
        last_component_type = '?'

        lev = -1
        for z in components_stack.items():
            last_lev = z[0]
            x = z[1]
            last_component = x[0]
            last_module = x[1]
            last_component_type = x[2]
            #print('==',x[0],x[1],x[2])
            if x[0] == component_name and x[1] == active_module:
                lev = z[0]
                component_name = x[0]
                module_name = x[1]
                component_type = x[2]
        
        #if not found or not privided take the last
        if lev == -1 : 
            lev = last_lev
            component_name = last_component
            module_name = last_module
            component_type = last_component_type

        offset = set_offset(lev-1)

        retrieve_activecomponent_debug_info(module_name, component_name, component_type)
        if (active_component_debug_enabled and active_component_debug_level > 0) or debug_log_services_level.find('BEGIN-END')>=0:
            if component_type:
                ctype = component_type + '-'
            else:
                ctype = ''
            msg = '{}finish [{}] from'.format(ctype, component_name)
            message = formatted_message(msg=msg)
            print(message)
    
        rem = 0
        for x in components_stack.items():
            if x[0] >= lev:
                rem = rem +1
            else:        
                level = x[0]

        #print('rem',rem,level)
        i = 1
        while i <= rem:
            components_stack.popitem()    
            i = i + 1

        level = 0
        for z in components_stack.items():
            level = z[0]
            x = z[1]
            active_component = x[0]
            active_module = x[1]
            active_component_type = x[2]

        offset = set_offset(level)
 #########################################
def set_offset(lev):
    global offset
    global offset_char
    global offset_tab
    offset = ''
    offset = offset_char*(lev)*offset_tab
    pfx = ''
    if prefix_timestamp:
        pfx = datetime.now().strftime("%d.%b %Y %H:%M:%S")
    if prefix:
        pfx = pfx + ' '+ prefix
    if pfx:
        offset = pfx + offset    
    offset = offset.lstrip()
    set_trailer()
    return offset
##########################################
def set_trailer():
    global trailer
    global suffix
    global suffix_timestamp
    global level
    trailer = ''
    if suffix:
        trailer = suffix
    if suffix_timestamp:
        trailer = trailer + ' '+datetime.now().strftime("%d.%b %Y %H:%M:%S")
    trailer = trailer.lstrip()
##########################################
def log_module_start(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_start(component_name, component_type='module')
##########################################
def log_module_finish(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_finish(component_name, component_type='module')
##########################################
def log_route_start(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_start(component_name, component_type='route')
##########################################
def log_route_finish(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_finish(component_name, component_type='route')
##########################################
def log_view_start(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_start(component_name, component_type='view')
##########################################
def log_view_finish(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_finish(component_name, component_type='view')
##########################################
def log_request_start(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_start(component_name, component_type='request')
##########################################
def log_request_finish(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_finish(component_name, component_type='request')
##########################################
def log_function_start(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_start(component_name, component_type='function')
##########################################
def log_function_finish(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_finish(component_name, component_type='function')
##########################################
def log_process_start(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_start(component_name, component_type='process')
##########################################
def log_process_finish(component_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    log_finish(component_name, component_type='process')
###############################################
###############################################
###############################################
### debug formatting configuration commands ###
###############################################
###############################################
###############################################
##########################################
def set_log_prefix(sid, uid):
    global sessionID
    global UserID
    global prefix
    global level
    global active_module
    global caller
    global offset
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']

    sessionID = sid
    userID = uid
    prefix = ''
    if sid:
        prefix = sid
    if uid:
        if prefix:
            prefix = prefix + ' | '+uid+'|'
        else:
            prefix = uid
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log debug prefix set to {}'.format(prefix)
        log_info(message)
##########################################
def set_log_suffix(sid, uid):
    global sessionID
    global UserID
    global suffix
    global level
    global level
    global active_module
    global caller
    global offset
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']

    sessionID = sid
    userID = uid
    suffix = ''
    if sid:
        suffix = sid
    if uid:
        if suffix:
            suffix = suffix + ' | '+uid+'|'
        else:
            suffix = uid
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log_suffix set to {}'.format(suffix)
        log_info(message)
##########################################
def set_log_suffix_timestamp(o='ON'):
    global suffix_timestamp
    global level
    global level
    global active_module
    global caller
    global offset
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    suffix_timestamp = False
    OnOff = "OFF"
    if o in ['ON', 1, '1', 'YES', 'Y', True]:
        suffix_timestamp = True
        OnOff = "ON"
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log debug suffix timestamp set {}'.format(OnOff)
        log_info(message)
##########################################
def set_log_prefix_timestamp(o='ON'):
    global prefix_timestamp
    global level
    global level
    global active_module
    global caller
    global offset
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    prefix_timestamp = False
    OnOff = "OFF"
    if o in ['ON', 1, '1', 'YES', 'Y', True]:
        prefix_timestamp = True
        OnOff = "ON"
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log debug prefix timestamp set {}'.format(OnOff)
        log_info(message)
##########################################
##########################################
##########################################
### modules config                     ###
##########################################
##########################################
##########################################
def set_module_debug_off(module_name):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    set_debug_level(module=module_name, component='', priority=1, debugOnOff='OFF')
    message = 'log debug set OFF for module {}'.format(module_name)
    log_info(message)
##########################################
def set_module_debug_on(module_name):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    set_debug_level(module=module_name, component='', priority=1, debugOnOff='ON')
    message = 'log debug set ON for module {}'.format(module_name)
    log_info(message)
##########################################
def set_module_debug_level(module_name='', debug_level=9):
    global active_module
    global caller
    global active_component_debug_enabled
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    retrieve_activecomponent_debug_info(module_name=module_name)
    onoff = 'OFF'
    if active_component_debug_enabled:
        onoff = 'ON'
    retrieve_activecomponent_debug_info()
    set_debug_level(module=module_name, priority=10, debugOnOff=onoff, debugLevel=debug_level)
    message = 'log debug level set to {}-{} for module {}'.format(onoff, debug_level, module_name)
    log_info(message)
##########################################

##########################################
##########################################
##########################################
### components config                  ###
##########################################
##########################################
##########################################
def set_component_debug_off(component_name='', module_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    set_debug_level(module=module_name, component=component_name, priority=2, debugOnOff='OFF')
    message = 'log debug set OFF for component {}.{}'.format(module_name, component_name)
    log_info(message)
##########################################
def set_component_debug_on(component_name='', module_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    set_debug_level(module=module_name, component=component_name, priority=2, debugOnOff='ON')
    message = 'log debug set ON for component {}.{}'.format(module_name, component_name)
    log_info(message)
##########################################
def set_component_debug_level(component_name='', debug_level=9, module_name=''):
    global active_module
    global caller
    global active_component_debug_enabled
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    retrieve_activecomponent_debug_info(module_name=module_name, component_name=component_name)
    onoff = 'OFF'
    if active_component_debug_enabled:
        onoff = 'ON'
    retrieve_activecomponent_debug_info()
    set_debug_level(module=module_name, component=component_name, priority=2, debugOnOff=onoff, debugLevel=debug_level)
    message = 'log debug level set to {}-{} for component {}.{}'.format(onoff, debug_level, module_name, component_name)
    log_info(message)
##########################################

##########################################
##########################################
##########################################
### component types config             ###
##########################################
##########################################
##########################################
def set_componenttype_debug_off(component_type='', component_name='', module_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    set_debug_level(module=module_name, component=component_name, component_type=component_type, priority=3, debugOnOff='OFF')
    message = 'log debug set OFF for component type {}.{}.{}'.format(module_name, component_name,component_type)
    log_info(message)
##########################################
def set_componenttype_debug_on(component_type='', component_name='', module_name=''):
    global active_module
    global caller
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    set_debug_level(module=module_name, component=component_name, component_type=component_type, priority=3, debugOnOff='ON')
    message = 'log debug set ON for component type {}.{}.{}'.format(module_name, component_name,component_type)
    log_info(message)
##########################################
def set_componenttype_debug_level(component_type='', component_name='', debug_level=9, module_name=''):
    global active_module
    global caller
    global active_component_debug_enabled
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    retrieve_activecomponent_debug_info(module_name=module_name, component_name=component_name, component_type=component_type)
    onoff = 'OFF'
    if active_component_debug_enabled:
        onoff = 'ON'
    retrieve_activecomponent_debug_info()
    set_debug_level(module=module_name, component=component_name, component_type=component_type, priority=3, debugOnOff=onoff, debugLevel=debug_level)
    message = 'log debug level set to {}-{} for component type {}.{}.{}'.format(onoff, debug_level, module_name, component_name, component_type)
    log_info(message)
##########################################
def set_global_debug(onoff='ON'):
    global global_debug_enabled 
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        global_debug_enabled = True
        message = 'global debug set ON'
    else:
        global_debug_enabled = False
        message = 'global debug set OFF'
    log_system_message(message)
##########################################
def set_debug_log_services_level(lev='WARNING'): #WARNING , ERROR, INFO, BEGIN-END VARIABLE PARAMETER URL
    lev = lev.upper()
    debug_log_services_level = lev
    message = 'debug_log_services_level set to {}'.format(debug_log_services_level)
    log_system_message(message)
##########################################
def set_debug_log_services_level_remove(lev='WARNING'):
    lev = lev.upper()
    debug_log_services_level = debug_log_services_level.replace(lev,'')
    message = 'debug_log_services_level set to {}'.format(debug_log_services_level)
    log_system_message(message)
##########################################
def set_debug_log_services_level_add(lev='WARNING'):
    lev = lev.upper()
    if debug_log_services_level.find(lev) < 0:
        debug_log_services_level = debug_log_services_level + ';' + lev
    message = 'debug_log_services_level set to {}'.format(debug_log_services_level)
    log_system_message(message)
##########################################
def set_log_message_compress_onoff(onoff='OFF'):
    global message_compressed_enabled 
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        message_compressed_enabled = True
        message = 'message compress set ON'
    else:
        message_compressed_enabled = True
        message = 'message compress set OFF'
    log_system_message(message)
##########################################
def set_log_moduletrace_onoff(onoff):
    global module_trace_enabled 
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        module_trace_enabled = True
        message = 'module_trace set ON'
    else:
        module_trace_enabled = False
        message = 'module_trace set OFF'
    log_system_message(message)
##########################################
def set_log_moduletrace_maxlength(len=40):
    global max_module_trace_length
    max_module_trace_length = len
    message = 'module_trace_length set to {}'.format(len)
    log_system_message(message)
##########################################
def set_log_message_maxlength(len=120):
    global max_message_length
    max_message_length = len
    message = 'message_length set to {}'.format(len)
    log_system_message(message)
##########################################
def set_log_message_maxlinelength(len=160):
    global max_line_length
    max_line_length = len
    message = 'message_line_length set to {}'.format(len)
    log_system_message(message)
##########################################
def set_log_message_format(fmt='FIX-MESSAGE'):
    global message_display_mode
    #'FIX-MESSAGE' #'FIXED-MODULE' #'FIX-MESSAGE' #'FIXED-LINE' #'FLOAT'
    fmt = fmt.upper()
    if fmt.find('FIX') >= 0:
        if fmt.find('MES') >= 0 or fmt.find('MSG') >= 0:
            fmt = 'FIX-MESSAGE'
        elif fmt.find('LIN') >= 0:
            fmt = 'FIX-LINE'
        elif fmt.find('MOD') >= 0 or fmt.find('TRAC') >= 0:
            fmt = 'FIX-MODULE'
        else:
            fmt = 'FIX-MESSAGE'
    else:
        fmt = 'FLOAT'
    message_display_mode = fmt.upper()
    message = 'message_display_mode set to {}'.format(fmt)
    log_system_message(message)

def set_log_message_prefix(prfix=''):
    global message_prefix
    message_prefix = prfix
    message = 'message_prefix set to [{}]'.format(prfix)
    log_system_message(message)

def set_log_system_message_prefix(prfix=''):
    global system_message_prefix
    system_message_prefix = prfix
    message = 'system_message_prefix set to [{}]'.format(prfix)
    log_system_message(message)
##########################################
##########################################
##########################################
### support functions                  ###
##########################################
##########################################
##########################################
def init_this_module():
    global thisModule
    global components_stack
    caller = sys._getframe(1)  # Obtain calling frame
    thisModule = caller.f_globals['__name__']
    message = 'log debug module set to ({})'.format(thisModule)
    log_system_message(message)
    components_stack = {}
##########################################
def set_debug_defaults(onoff='ON', debuglevel=9):
    global default_debug_onoff
    global default_debug_level
    global active_module
    global caller
    global offset
    xcaller = sys._getframe(1)  # Obtain calling frame
    xactive_moduleX = xcaller.f_globals['__name__']
    if thisModule != xactive_moduleX:
        caller = xcaller
        active_module = xactive_moduleX
    default_debug_level = debuglevel
    default_debug_onoff = False
    default_debug_onoff_Str = 'OFF'
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        default_debug_onoff = True
        default_debug_onoff_Str = 'ON'
    message = 'log debug defaults set to ({}-{})'.format(default_debug_onoff_Str, default_debug_level)
    log_info(message)

##########################################
def config_from_environment_variables():
    for item in os.environ:
        if item.upper().find('DEBUG_') == 0:
            what = item.upper().replace('DEBUG_', '').lower()
            val = os.environ.get(item).upper()
            if val not in ('OFF', 'ON'):
                valonoff = 'OFF'
            else:
                valonoff = val
            #print(item, what, val)
            if what.upper().find('MODULE_') == 0:
                typ = 'MODULE'
                name = what.upper().replace('MODULE_', '').lower()
                #print(item, what, typ, name, valonoff)
                set_debug_level(module=name, debugOnOff=valonoff, debugLevel=9)
            elif what.upper().find('FOLDER_') == 0:
                typ = 'FOLDER'
                name = what.upper().replace('FOLDER_', '').lower()
                #print(item, what, typ, name, valonoff)
                set_debug_level(folder=name, debugOnOff=valonoff, debugLevel=9)
            elif what.upper().find('TYPE_') == 0:
                typ = 'COMPONENT_TYPE'
                name = what.upper().replace('TYPE_', '').lower()
                set_debug_level(component_type=name, debugOnOff=valonoff, debugLevel=9)
                #print(item, what, typ, name, valonoff)
            elif what.upper().find('LEVEL') == 0:
                typ = 'LEVEL'
                name = name.upper().replace('LEVEL', '').lower()
                #print(item, what, typ, name, val)
                if name.upper().find('_ADD') == 0:
                    set_debug_log_services_level_add(lev=val)
                elif name.upper().find('_REMOVE') == 0:
                    set_debug_log_services_level_remove(lev=val)
                else:
                    set_debug_log_services_level(lev=val)
            elif what.upper().find('GLOBAL') == 0:
                typ = 'GLOBAL_DEBUG'
                name = ''
                #print(item, what, typ, name, valonoff)
                set_global_debug(valonoff)
            elif what.upper().find('DEFAULT') == 0:
                typ = 'DEFAULTS'
                name = ''
                #print(item, what, typ, name, valonoff)
                set_debug_defaults(onoff=valonoff, debuglevel=9)
            elif what.upper().find('TIMESTAMP') == 0:
                typ = 'TIMESTAMP'
                name = name.upper().replace('TIMESTAMP', '').lower()
                #print(item, what, typ, name, valonoff)
                if name.upper().find('_LEFT') == 0:
                    set_log_prefix_timestamp(valonoff)
                else:
                    set_log_suffix_timestamp(valonoff)
            elif what.upper().find('MODULE_TRACE') == 0:
                typ = 'MODULE_TRACE'
                name = name.upper().replace('MODULE_TRACE', '').lower()
                #print(item, what, typ, name, valonoff)
                set_log_moduletrace_onoff(valonoff)
            elif what.upper().find('MESSAGE_COMPRESS') == 0:
                typ = 'MESSAGE_COMPRESS'
                name = name.upper().replace('MESSAGE_COMPRESS', '').lower()
                #print(item, what, typ, name, valonoff)
                set_log_message_compress_onoff(valonoff)
            elif what.upper().find('MAX_MESSAGE_LENGTH') == 0:
                typ = 'MAX_MESSAGE_LENGTH'
                name = name.upper().replace('MAX_MESSAGE_LENGTH', '').lower()
                #print(item, what, typ, name, valonoff)
                mlen = int(val)
                set_log_message_maxlength(mlen)
            elif what.upper().find('MAX_MODULETRACE_LENGTH') == 0:
                typ = 'MAX_MODULETRACE_LENGTH'
                name = name.upper().replace('MAX_MODULETRACE_LENGTH', '').lower()
                #print(item, what, typ, name, valonoff)
                mlen = int(val)
                set_log_moduletrace_maxlength(mlen)
            else:
                typ = 'COMPONENT'
                name = what.lower()
                #print(item, what, typ, name, valonoff)
                set_debug_level(component=name, debugOnOff=valonoff, debugLevel=9)
##########################################
# take second element for sort
def takeSecond(elem):
    return elem[1]
##########################################
def set_debug_level(folder='*', module='*', component='*', component_type='*', priority=0, debugOnOff='ON', debugLevel=9):
    global active_module
    global caller
    global offset
    global Components
    xcaller = sys._getframe(1)  # Obtain calling frame
    xactive_moduleX = xcaller.f_globals['__name__']
    if thisModule != xactive_moduleX:
        caller = xcaller
        active_module = xactive_moduleX

    componentKey = folder+'.'+module+'.'+component+'.'+component_type
    CalculatedPriority = 0
    if folder not in ('', '*'):
        CalculatedPriority = CalculatedPriority + 100
    if module not in ('', '*'):
        CalculatedPriority = CalculatedPriority + 100
    if component not in ('', '*'):
        CalculatedPriority = CalculatedPriority + 100
    if component_type not in ('', '*'):
        CalculatedPriority = CalculatedPriority + 100
    CalculatedPriority = CalculatedPriority+priority

    if debugOnOff in ['ON', 1, '1', 'YES', 'Y', True]:
        debugOnOff = True
        debugOnOff_Str = 'ON'
    else:
        debugOnOff = False
        debugOnOff_Str = 'OFF'
    found = False
    for ix, item in enumerate(Components):
        if item[0] == componentKey:
            Components[ix] = [componentKey, CalculatedPriority, debugOnOff_Str, debugOnOff, debugLevel, folder, module, component, component_type]
            found = True
            #print(ix,componentKey,'already')
    if not found:
        Components.append([componentKey, CalculatedPriority, debugOnOff_Str, debugOnOff, debugLevel, folder, module, component, component_type])

    # sort list with key the second array element which is the priority
    Components.sort(key=takeSecond, reverse=False) 
    #ModulesDictionary.update({componentKey:[debugOnOff, debugLevel]})
    #print(ModulesDictionary)
    if component_type and component_type != '*':
        cfgkey = 'DEBUG_'+component_type.upper()
        os.environ[cfgkey] = debugOnOff_Str.upper()
        message = 'environment variable {} set to {}'.format(cfgkey, debugOnOff_Str)
        log_system_message(message)

    message = 'debug levels for folder "{}" module "{}" component "{}" compo-type "{}" set to ({}-{}) priority {}.'.format(folder, module, component, component_type, debugOnOff_Str, debugLevel, CalculatedPriority)
    log_system_message(message)
##########################################
def retrieve_activecomponent_debug_info(folder_name='', module_name='', component_name='', component_type=''):
    global ModulesDictionary
    global Components
    global active_folder
    global active_module
    global active_component
    global active_component_type
    global last_active_module
    global active_component_debug_enabled
    global active_component_debug_level
    global default_debug_onoff
    global default_debug_level
    if not global_debug_enabled:
        active_component_debug_enabled = False
        active_component_debug_level = 0
        #print ('===global_debug_enabled is OFF')
        return

    if not folder_name:
        folder_name = active_folder
    if not module_name:
        module_name = active_module
    if not component_name:
        component_name = active_component
    if not component_type:
        component_type = active_component_type
    if not(folder_name):
        folder_name = '*'
    if not(module_name):
        module_name = '*'
    if not(component_name):
        component_name = '*'
    if not(component_type):
        component_type = '*'

    activeKey = module_name+'.'+component_name+'.'+component_type
    #print('search for ',activeKey)
    #weighted_matches = []
    found = False
    for ix, moduleArray in enumerate(Components):
        module = moduleArray[0]
        # print(ix, module,'----------------------------------------------')
        # print (ix, 'folder',folder_name,'-->',moduleArray[5])
        # print (ix, 'module',module_name,'-->',moduleArray[6])
        # print (ix, 'component',component_name,'-->',moduleArray[7])
        # print (ix, 'type',component_type,'-->',moduleArray[8])
        # wrkmodule = module
        priority = moduleArray[1]
        onoffStr = moduleArray[2]
        onoff = moduleArray[3]
        debuglevel = moduleArray[4]
        match = False
        px=''
        # print(ix,module_name,moduleArray[6])
        # print(ix, str('.'+module_name+'.').find(str('.'+moduleArray[6]+'.')))
        # print(ix, str('.'+moduleArray[6]+'.').find(str('.'+module_name+'.')))
        if folder_name == moduleArray[5] or moduleArray[5] in ('', '*'):
            if module_name == moduleArray[6] or moduleArray[6] in ('', '*') \
            or str('.'+module_name+'.').find(str('.'+moduleArray[6]+'.')) \
            or str('.'+moduleArray[6]+'.').find(str('.'+module_name+'.')) >= 0:
                # print(ix,module_name,moduleArray[6])
                # print(ix, str('.'+module_name+'.').find(str('.'+moduleArray[6]+'.')))
                # print(ix, str('.'+moduleArray[6]+'.').find(str('.'+module_name+'.')))
                if component_name == moduleArray[7] or moduleArray[7] in ('', '*'):
                    if component_type == moduleArray[8] or moduleArray[8] in ('', '*'):
                        match = True

        # m = module.replace('*', r'[\w]*')
        # m = m.replace('.', r'\.')
        # p0 = r'^' + m + r'\.[\w.]*'
        # p1 = r'[\w.]*' + m + r'\.[\w.]*'
        # p2 = r'[\w.]*\.' + m + r'[\w.]*'
        # px = r'[\w.]*\.' + m + r'[\w.]*'
        # px = r'[\w.]*\.' + m
        # match = re.search(px, activeKey)
        # #print(activeKey.find(module+'.'))
        # #print(activeKey.find('.'+module+'.'), activeKey, module)
        # wrkmodule=module.replace(activeKey,'')
        # wrkmodule=module.replace('*','')
        # wrkmodule=module.replace('.','')
        # print(activeKey, module, '-->', wrkmodule)
        
        # match0 = re.search(p0, activeKey)
        # match1 = re.search(p1, activeKey)
        # if match1:
        #     print (match1.group())
        # else:
        #     print('no match',p1)
        # match2 = re.search(p2, activeKey)
        # if match2:
        #     print (match2.group())
        # else:
        #     print('no match',p2)
        #if match0 or match1 or match2:

        if match:
            found = True
            #print ('===FOUND', ix, activeKey,'-->',px, '-->', module, 'MATCHED', onoff, debuglevel)
            # print ('folder',folder_name,'-->',moduleArray[5])
            # print ('module',module_name,'-->',moduleArray[6])
            # print ('component',component_name,'-->',moduleArray[7])
            # print ('type',component_type,'-->',moduleArray[8])
            active_component_debug_enabled = onoff
            active_component_debug_level = debuglevel
        #else:
            #print ('xxxx', activeKey, i, module, 'NOT MATCHED')
    if not found:
        active_component_debug_enabled = default_debug_onoff
        active_component_debug_level = default_debug_level
        #print('===NOT-FOUND', activeKey, active_component_debug_enabled, active_component_debug_level)
#############################################################
def formatted_message(msg='?', p1='', p2='', p3='', p4='', p5=''):
    global offset
    global active_module
    global max_message_length
    global max_module_trace_length
    global max_line_length
    global message_display_mode
    global message_prefix
    global system_message_prefix

    message = '{}{}{}'.format(message_prefix, offset, msg)
    if p1:
        message = message + ' {}'.format(p1)
    if p2:
        message = message + ' {}'.format(p2)
    if p3:
        message = message + ' {}'.format(p3)
    if p4:
        message = message + ' {}'.format(p4)
    if p5:
        message = message + ' {}'.format(p5)
    
    global max_message_length
    global max_module_trace_length
    global max_line_length
    global message_display_mode

    #method 1
    if message_display_mode.upper() == 'FIX-MESSAGE':
        msg1 = message[0:max_message_length]
        len_left = len(msg1)
        len_spaces = max_message_length - len_left
        msg = '{}{}'.format(msg1, ' '*len_spaces)
        msg = msg[0:max_message_length]

        right_len = max_line_length - max_message_length - 3
        len_right = len(active_module)
        if len_right > right_len:
            ofs = len_right - right_len + 4
            mod = '...' + active_module[ofs:len_right]
        else:
            mod = active_module
        mod = mod[0:right_len]
        formatted_message = '{}[{}]'.format(msg, mod)
    elif message_display_mode.upper() == 'FIX-MODULE':
        #method 2:
        msg_len = max_line_length - max_module_trace_length - 3
        msg1 = message[0:msg_len]
        len_left = len(msg1)
        len_spaces = msg_len - len_left
        if len_spaces > 0:
            msg = '{}   {}'.format(msg1, ' '*len_spaces)
        else:
            msg = '{}...'.format(msg1)

        right_len = max_module_trace_length
        len_right = len(active_module)
        if len_right > right_len:
            ofs = len_right - right_len + 3
            mod = '...' + active_module[ofs:len_right]
        else:
            mod = active_module
        formatted_message = '{}[{}]'.format(msg, mod)
    elif message_display_mode.upper() == 'FIX-LINE':
        #method 3:
        len_left = len(message)
        len_right = len(active_module)
        len_spaces = max_line_length - (len_left + len_right + 3)
        if len_spaces > 1:
            msg = '{}{}[{}]'.format(message, '.'*len_spaces, active_module)
        else:
            msg = '{}...[{}]'.format(message, active_module)
        formatted_message = msg[0:max_line_length]
    else:
        #method 3: floating msg (full)
        formatted_message = '{}...[{}]'.format(message, active_module)

    return formatted_message


##########################################
##########################################
##########################################
### initialization                     ###
##########################################
##########################################
##########################################
init_this_module()
##########################################
##########################################
##########################################
def testx():
    caller = sys._getframe(1)  # Obtain calling frame
    active_module = caller.f_globals['__name__']
    active_modulex = caller.f_locals['__name__']
    print(active_modulex, active_module)
    print('xxx',inspect.stack()[0][3])
    print('xxx',inspect.stack()[1][3])
    i=0
    while i<=5:
        print(i,'xxx[0]',inspect.stack()[0][i])
        i=i+1
    i=0
    while i<=5:
        print(i,'xxx[1]',inspect.stack()[1][i])
        i=i+1

if __name__ == '__main__':
    #tests
    #global Components
    set_debug_defaults(onoff='ON', debuglevel=9)
    set_debug_level(module='webapp', debugOnOff='OFF', debugLevel=9)
    set_debug_level(module='external_services', debugOnOff='OFF', debugLevel=9)
    set_debug_level(module='*', component='geolocation_services', priority=88, debugOnOff='OFF', debugLevel=1)
    set_debug_level(module='*', component='geolocation_services', component_type='view' , priority=89, debugOnOff='OFF', debugLevel=2)
    set_debug_level(module='*', component='log_services', priority=88, debugOnOff='ON', debugLevel=9)
    #print (Components)
    # i = 0
    # for x in Components:
    #     i=i+1
    #     print(i,x)
    active_module = 'a.b.geolocatioxn_services'
    retrieve_activecomponent_debug_info('view')
    print('result:', active_module, active_component_debug_enabled, active_component_debug_level)
    testx()
    # module = '*.*.geolocation_services.*'
    # m = module.replace('.', r'\.')
    # m = m.replace('*', r'[\w.]*')
    # p2 = r'[\w.]*\.' + m + r'[\w.]*'
    # p0 = r'^' + m + r'\.[\w.]*'
    # p1 = r'[\w.]*' + m + r'\.[\w.]*'
    # p1 = r'[\w.]*' + m + r'[\w.]*'
    # p=p1
    # match = re.search(p, active_module)
    # if match:
    #     print (match.group())
    # else:
    #     print('no match',p)

    # test={}
    # test.update({'*.b.c':['ON']})
    # x = 'a.b.c'
    # print (x)
    # print ('--',test.get(x))
    # set_log_prefix_timestamp(1)
    # set_log_prefix('SID-2','US01')
    # log_start('alpha')
    # log_info('test alpha.....')
    # log_variable('var', 'alpha')
    # log_start('beta')
    # log_variable('var', 'beta')
    # log_start('gama')
    # log_variable('var', 'gama')
    # log_finish('gama')
    # log_variable('var', 'beta')
    # log_finish('beta')
    # log_variable('var', 'alpha')
    # log_finish('alpha')
    # log_variable('test', 'test')

    # set_log_prefix_timestamp(0)
    # set_log_prefix('','')
    # set_log_suffix_timestamp(1)
    # #set_log_suffix('SID-x','xxx1')

    # log_start('alpha')
    # log_info('test alpha.....')
    # log_variable('var', 'alpha')
    # log_start('beta')
    # log_variable('var', 'beta')
    # log_start('gama')
    # log_variable('var', 'gama')
    # log_finish('gama')
    # log_variable('var', 'beta')
    # log_finish('beta')
    # log_variable('var', 'alpha')
    # log_finish('alpha')
    # log_variable('test', 'test')

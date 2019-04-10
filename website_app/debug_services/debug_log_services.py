import os
import sys
import re
import inspect
from datetime import datetime
from colorama import init as ColorsInit, Fore, Back, Style

global_debug_OFF = False
global_debug_enabled = True
debug_log_services_level = 'WARNING;ERROR;IMPORTANT'
default_debug_onoff = False
default_debug_level = 9
module_trace_enabled = True
message_compressed_enabled = False

xmodules = []

max_line_length = 133
max_message_length = 90
max_module_trace_length = 45
message_display_mode = 'FIX-MESSAGE'  #'FIX-MODULE' #'FIX-MESSAGE' #'FIX-LINE' #'FLOAT'
suffix_module = False
sid_prefix = False
sid_suffix = False
uid_prefix = False
uid_suffix = False

message_format = 'OFFSET PREFIX MESSAGE TIMESTAMP MODULE SUFFIX SID UID'
message_format_prefix = 'OFFSET PREFIX'
message_format_suffix = 'TIMESTAMP MODULE SUFFIX SID UID'
message_suffix = ''
message_prefix = ''
system_message_prefix = ' o '
debug_config_message_prefix = ' o '
debug_config_message_enabled = True
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
offset_enabled = True
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

global_counter = 0
prev_active_chain = '+'

active_color = Fore.RED
active_folder = ''
active_module = ''
active_component = ''
active_component_type = ''
#active_module_key = ''
#previous_module_key = ''
activeKey = ''
active_chain = ''
prevKey = ''

active_component_debug_enabled = False
active_component_debug_level = 9
##########################################
def log_info(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 0) or debug_log_services_level.find('INFO') >= 0:
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5,msgtype='info')
            print(message)
##########################################
def log_checkpoint(cp='', msg='', m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 0) or debug_log_services_level.find('CHECK') >= 0:
            msg1 = combined_message(msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            msg = ' @ checkpoint-{}:{}{}{}{}{}'.format(cp, Back.YELLOW, Fore.RED, msg1, Back.RESET, Fore.RESET)
            message = formatted_message(msg=msg, msgtype='checkpoint')
            print(message)
##########################################
def log_warning(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    # global offset
    # global trailer
    # global active_module
    # global caller
    # global debug_log_services_level
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        if (active_component_debug_enabled and active_component_debug_level > 1) \
            or debug_log_services_level.find('WARNING') >= 0 \
            or debug_log_services_level.find('INFO') >= 0:
            msg1 = combined_message(msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5)
            msg = 'warning:{}{}{}{}{}'.format(Back.YELLOW, Fore.RED, msg1, Back.RESET, Fore.RESET)
            message = formatted_message(msg=msg, msgtype='warning')
            #message = '{}{}{}{}'.format(Back.YELLOW, Fore.RED, message, Style.RESET_ALL) 
            print(message)
##########################################
def log_error(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        msg = 'ERROR:{}'.format(msg)
        message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='error', Nocolors=True)
        message = '{}{}{}{}'.format(Back.RED, Fore.WHITE, message, Style.RESET_ALL) 
        print(message)
##########################################
def log_system_message(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    global system_message_prefix
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    msg = '{}system-message:{}'.format(system_message_prefix, msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='system-message', Nocolors=True)
    message = '{}{}{}{}'.format(Back.GREEN, Fore.RED, message, Style.RESET_ALL) 
    print(message)
##########################################
def log_system_info(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    global system_message_prefix
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    msg = '{}system-info:{}'.format(system_message_prefix, msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='system-info', Nocolors=True)
    message = '{}{}{}{}'.format(Back.GREEN, Fore.YELLOW, message, Style.RESET_ALL) 
    print(message)
##########################################
def log_system_warning(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    global system_message_prefix
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    msg = '{}SYSTEM-WARNING:{}'.format(system_message_prefix, msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='system-warning', Nocolors=True)
    message = '{}{}{}{}'.format(Back.YELLOW, Fore.RED, message, Style.RESET_ALL) 
    print(message)
##########################################
def log_system_error(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    global system_message_prefix
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    msg = '{}SYSTEM-ERROR:{}'.format(system_message_prefix, msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='system-error', Nocolors=True)
    message = '{}{}{}{}'.format(Back.RED, Fore.WHITE, message, Style.RESET_ALL) 
    print(message)
##########################################
def log_debug_config_message(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    global debug_config_message_prefix
    global debug_config_message_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    msg = '{}{}'.format(debug_config_message_prefix, msg)
    message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='config-message', Nocolors=True)
    message = '{}{}{}{}'.format(Back.BLACK, Fore.WHITE, message, Style.RESET_ALL) 
    if debug_config_message_enabled:
        print(message)
##########################################
def log_variable(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('VARIABLE')>=0:
            msg = '{0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='variable')
            print(message)
##########################################
def log_variables(name='', value='', n2='', v2='', n3='', v3='', n4='', v4=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('VARIABLE')>=0:
            msg = '{}={}'.format(name, value)
            if n2 or v2:
                msg = '{}, {}={}'.format(msg, n2, v2)
            if n3 or v3:
                msg = '{}, {}={}'.format(msg, n3, v3)
            if n4 or v4:
                msg = '{}, {}={}'.format(msg, n4, v4)
            message = formatted_message(msg=msg, msgtype='variable')
            print(message)
##########################################
def log_env_param(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('VARIABLE')>=0:
            msg = 'env_param: {0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='env-param')
            print(message)
##########################################
def log_file(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) \
            or debug_log_services_level.find('VARIABLE') >=0 \
            or debug_log_services_level.find('FILE') >=0 \
            :
            msg = 'file-{0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='file')
            print(message)
##########################################
def log_variable_short(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('VARIABLE')>=0:
            valueStr = str(value)
            if len(valueStr)>37:
                valueStr = valueStr[0:37] + '...' 
            msg = '{0}={1}'.format(name, valueStr)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='variable')
            print(message)
##########################################
def log_param(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('PARAM')>=0:
            msg = 'param: {0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='param')
            print(message)
##########################################
def log_config_param(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 3) or debug_log_services_level.find('CONFIG') >= 0:
            msg = 'config_param: {0}={1}'.format(name, value)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='config-param')
            print(message)
##########################################
def log_important(msg, m1='', m2='', m3='', m4='', m5=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        if (active_component_debug_enabled and active_component_debug_level > 1) \
            or debug_log_services_level.find('IMPORTANT') >= 0 \
            or debug_log_services_level.find('WARNING') >= 0 \
            or debug_log_services_level.find('INFO') >= 0:
            msg = 'WARNING:{}'.format(msg)
            message = formatted_message(msg=msg, p1=m1, p2=m2, p3=m3, p4=m4, p5=m5, msgtype='important')
            print(message)
##########################################
def log_url_param(name='', value=''):
    global debug_log_services_level
    global active_component_debug_level
    global active_component_debug_enabled
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 2) or debug_log_services_level.find('URL')>=0:
            msg = 'url-param {0}={1}'.format(name, value)
            message = formatted_message(msg=msg, msgtype='url-param')
            print(message)
##########################################
def tispaolas(xcaller):
    global thisModule
    global caller 
    global active_folder
    global active_module
    global active_component
    global active_component_type
    global active_chain
    global prev_active_chain
    global global_counter
    global active_color
    #if global_debug_enabled:
    #xcaller = sys._getframe(1)  # Obtain calling frame
    xactive_moduleX = xcaller.f_globals['__name__']
    if thisModule != xactive_moduleX and xactive_moduleX != 'config':
        caller = xcaller
        #print('### (tispaolas) prev active_module:', active_module)
        active_module = xactive_moduleX
        active_module_key = active_module
        active_chain = active_component_type+':'+active_module+'.'+active_component
        #previous_module_key = ''

        #print('### (tispaolas) active_module:', active_module)
    #else:
        #print('### (tispaolas) internal call:', active_module)
    if active_chain != prev_active_chain:
        prev_active_chain = active_chain
        global_counter = global_counter + 1
        #active_color = component_color(global_counter)

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
    global active_color
    active_component = component_name
    active_component_type = component_type
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        level = level + 1
        active_color = component_color(global_counter)
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 0) or debug_log_services_level.find('BEGIN-END')>=0:
            if active_component_type:
                ctype = active_component_type + '-'
            else:
                ctype = ''
            msg = '{}start [{}]'.format(ctype, component_name)
            #msg = Fore.GREEN+'{}start [{}]'.format(ctype, component_name)+Style.RESET_ALL
            #msg = 'warning:{}{}{}{}'.format(Back.YELLOW, Fore.RED, msg, Style.RESET_ALL) 
            message = formatted_message(msg=msg, msgtype='START')
            print(message)

        components_stack.update({level : [active_component, active_module, active_component_type, active_color]})
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
    global debug_log_services_level
    global active_color
    active_component = component_name
    active_component_type = component_type
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    if global_debug_enabled:
        last_lev = -1
        last_component = '?'
        last_module = '?'
        last_component_type = '?'
        last_component_color = Fore.WHITE

        lev = -1
        for z in components_stack.items():
            last_lev = z[0]
            x = z[1]
            last_component = x[0]
            last_module = x[1]
            last_component_type = x[2]
            last_component_color = x[3]
            ##print('==',x[0],x[1],x[2],x[3])
            if x[0] == component_name and x[1] == active_module:
                lev = z[0]
                component_name = x[0]
                module_name = x[1]
                component_type = x[2]
                component_color = x[3]
        
        #if not found or not privided take the last
        if lev == -1: 
            lev = last_lev
            component_name = last_component
            module_name = last_module
            component_type = last_component_type
            component_color = last_component_color

        offset = set_offset(lev-1)
        prev_active_color = active_color
        active_color = component_color
        retrieve_activecomponent_debug_info()
        if (active_component_debug_enabled and active_component_debug_level > 0) or debug_log_services_level.find('BEGIN-END')>=0:
            if component_type:
                ctype = component_type + '-'
            else:
                ctype = ''
            #col = component_color(lev-1)
            msg = '{}finish [{}]'.format(ctype, component_name)
            #msg = Fore.RED+'{}finish [{}]'.format(ctype, component_name)+Style.RESET_ALL
            message = formatted_message(msg=msg, msgtype='FINISH')
            print(message)
    
        rem = 0
        for x in components_stack.items():
            if x[0] >= lev:
                rem = rem +1
            else:        
                level = x[0]

        ##print('rem',rem,level)
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
            active_color = x[3]

        offset = set_offset(level)
 #########################################
def set_offset(lev):
    global offset
    global offset_char
    global offset_tab
    offset = ''
    #offset = offset_char*(lev)*offset_tab
    offset = '>'*(lev)*offset_tab
    # pfx = ''
    # if prefix_timestamp:
    #     pfx = datetime.now().strftime("%d.%b %Y %H:%M:%S")
    # if prefix:
    #     pfx = pfx + ' '+ prefix
    # if pfx:
    #     offset = pfx + offset    
    offset = offset.lstrip()
    #set_trailer()
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
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_start(component_name, component_type='module')
##########################################
def log_module_finish(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_finish(component_name, component_type='module')
##########################################
def log_route_start(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_start(component_name, component_type='route')
##########################################
def log_route_finish(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_finish(component_name, component_type='route')
##########################################
def log_view_start(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_start(component_name, component_type='view')
##########################################
def log_view_finish(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_finish(component_name, component_type='view')
##########################################
def log_request_start(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_start(component_name, component_type='request')
##########################################
def log_request_finish(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_finish(component_name, component_type='request')
##########################################
def log_function_start(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_start(component_name, component_type='function')
##########################################
def log_function_finish(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_finish(component_name, component_type='function')
##########################################
def log_process_start(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_start(component_name, component_type='process')
##########################################
def log_process_finish(component_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    log_finish(component_name, component_type='process')
###################shalimar#######################
def log_file_start(file=__file__, component_name=''):
    global active_module
    global active_folder
    global active_component
    global active_component_type
    #print('f=',file)
    thisfile = os.path.abspath(file)
    thisDir = os.path.dirname(file)
    #print('d=',thisDir)
    thisFileName = os.path.basename(file)
    #print('fnm=', thisFileName)
    file_name = os.path.splitext(thisFileName)[0]
    thisFolderName = os.path.basename(thisDir)
    #print('fonm=',thisFolderName)
    exec_folder = os.path.abspath(os.path.dirname(file))
    #print('x=',exec_folder)
    app_config_folder = os.path.dirname(exec_folder)
    #print('xx=',app_config_folder)
    active_module = thisFolderName+'.'+file_name
    active_component = component_name
    active_component_type = 'file'
    active_folder = exec_folder
    log_start(component_name, component_type='file')
###################shalimar#######################
def log_file_finish(file=__file__, component_name=''):
    global active_module
    global active_folder
    global active_component
    global active_component_type
    #print('f=',file)
    thisfile = os.path.abspath(file)
    thisDir = os.path.dirname(file)
    #print('d=',thisDir)
    thisFileName = os.path.basename(file)
    #print('fnm=', thisFileName)
    file_name = os.path.splitext(thisFileName)[0]
    thisFolderName = os.path.basename(thisDir)
    #print('fonm=',thisFolderName)
    exec_folder = os.path.abspath(os.path.dirname(file))
    #print('x=',exec_folder)
    app_config_folder = os.path.dirname(exec_folder)
    #print('xx=',app_config_folder)
    active_module = thisFolderName+'.'+file_name
    active_component = component_name
    active_component_type = 'file'
    active_folder = exec_folder
    log_finish(component_name, component_type='file')
###############################################
def log_config_start(file=__file__, component_name=''):
    global active_module
    global active_folder
    global active_component
    global active_component_type
    #print('f=',file)
    thisfile = os.path.abspath(file)
    thisDir = os.path.dirname(file)
    #print('d=',thisDir)
    thisFileName = os.path.basename(file)
    #print('fnm=', thisFileName)
    file_name = os.path.splitext(thisFileName)[0]
    thisFolderName = os.path.basename(thisDir)
    #print('fonm=',thisFolderName)
    exec_folder = os.path.abspath(os.path.dirname(file))
    #print('x=',exec_folder)
    app_config_folder = os.path.dirname(exec_folder)
    #print('xx=',app_config_folder)
    active_module = thisFolderName+'.'+file_name
    active_component = component_name
    active_component_type = 'configuration'
    active_folder = exec_folder
    log_start(component_name, component_type='configuration')
###################shalimar#######################
def log_config_finish(file=__file__, component_name=''):
    global active_module
    global active_folder
    global active_component
    global active_component_type
    #print('f=',file)
    thisfile = os.path.abspath(file)
    thisDir = os.path.dirname(file)
    #print('d=',thisDir)
    thisFileName = os.path.basename(file)
    #print('fnm=', thisFileName)
    file_name = os.path.splitext(thisFileName)[0]
    thisFolderName = os.path.basename(thisDir)
    #print('fonm=',thisFolderName)
    exec_folder = os.path.abspath(os.path.dirname(file))
    #print('x=',exec_folder)
    app_config_folder = os.path.dirname(exec_folder)
    #print('xx=',app_config_folder)
    active_module = thisFolderName+'.'+file_name
    active_component = component_name
    active_component_type = 'configuration'
    active_folder = exec_folder
    log_finish(component_name, component_type='configuration')
###############################################
###############################################
def log_init_start(file=__file__, component_name=''):
    global active_module
    global active_folder
    global active_component
    global active_component_type
    #print('f=',file)
    thisfile = os.path.abspath(file)
    thisDir = os.path.dirname(file)
    #print('d=',thisDir)
    thisFileName = os.path.basename(file)
    #print('fnm=', thisFileName)
    file_name = os.path.splitext(thisFileName)[0]
    thisFolderName = os.path.basename(thisDir)
    #print('fonm=',thisFolderName)
    exec_folder = os.path.abspath(os.path.dirname(file))
    #print('x=',exec_folder)
    app_config_folder = os.path.dirname(exec_folder)
    #print('xx=',app_config_folder)
    active_module = thisFolderName+'.'+file_name
    active_component = component_name
    active_component_type = 'initialization'
    active_folder = exec_folder
    log_start(component_name, component_type='initialization')
###################shalimar#######################
def log_init_finish(file=__file__, component_name=''):
    global active_module
    global active_folder
    global active_component
    global active_component_type
    #print('f=',file)
    thisfile = os.path.abspath(file)
    thisDir = os.path.dirname(file)
    #print('d=',thisDir)
    thisFileName = os.path.basename(file)
    #print('fnm=', thisFileName)
    file_name = os.path.splitext(thisFileName)[0]
    thisFolderName = os.path.basename(thisDir)
    #print('fonm=',thisFolderName)
    exec_folder = os.path.abspath(os.path.dirname(file))
    #print('x=',exec_folder)
    app_config_folder = os.path.dirname(exec_folder)
    #print('xx=',app_config_folder)
    active_module = thisFolderName+'.'+file_name
    active_component = component_name
    active_component_type = 'initialization'
    active_folder = exec_folder
    log_finish(component_name, component_type='initialization')
###############################################
###############################################
###############################################
### debug formatting configuration commands ###
###############################################
###############################################
###############################################
###############################################
def set_log_prefix(sid, uid):
    global sessionID
    global UserID
    global prefix
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
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
    set_debug_log_message_format()
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log debug prefix set to {}'.format(prefix)
        log_info(message)
##########################################
def set_log_suffix(sid, uid):
    global sessionID
    global UserID
    global suffix
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)

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
    set_debug_log_message_format()
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log_suffix set to {}'.format(suffix)
        log_info(message)
##########################################
def set_log_suffix_timestamp(o='ON'):
    global suffix_timestamp
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    suffix_timestamp = False
    OnOff = "OFF"
    if o in ['ON', 1, '1', 'YES', 'Y', True]:
        suffix_timestamp = True
        OnOff = "ON"
    set_debug_log_message_format()
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log debug suffix timestamp set {}'.format(OnOff)
        log_info(message)
##########################################
def set_log_prefix_timestamp(o='ON'):
    global prefix_timestamp
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    prefix_timestamp = False
    OnOff = "OFF"
    if o in ['ON', 1, '1', 'YES', 'Y', True]:
        prefix_timestamp = True
        OnOff = "ON"
    set_debug_log_message_format()
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log debug prefix timestamp set {}'.format(OnOff)
        log_info(message)
##########################################
def set_log_timestamp_ONOFF(o='ON',position='SUFFIX'):
    global prefix_timestamp
    global suffix_timestamp
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    prefix_timestamp = False
    suffix_timestamp = False
    message = 'log debug timestamp set OFF'
    OnOff = "OFF"
    if position == 'PREFIX':
        pos = 'prefix'
        if o in ['ON', 1, '1', 'YES', 'Y', True]:
            prefix_timestamp = True
            OnOff = "ON"
            message = 'log debug prefix timestamp set ON '
    else:
        pos = 'suffix'
        if o in ['ON', 1, '1', 'YES', 'Y', True]:
            suffix_timestamp = True
            OnOff = "ON"
            message = 'log debug suffix timestamp set ON '
    set_debug_log_message_format()
    if active_component_debug_enabled and active_component_debug_level > 0:
        log_info(message)
##########################################
def set_log_suffix_module_ONOFF(o='ON'):
    global suffix_module
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    suffix_module = False
    OnOff = "OFF"
    if o in ['ON', 1, '1', 'YES', 'Y', True]:
        suffix_module = True
        OnOff = "ON"
    set_debug_log_message_format()
    if active_component_debug_enabled and active_component_debug_level > 0:
        message = 'log debug suffix module set {}'.format(OnOff)
        log_info(message)
def set_log_moduletrace_onoff(onoff):
    global module_trace_enabled 
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        module_trace_enabled = True
        message = 'module_trace set ON'
    else:
        module_trace_enabled = False
        message = 'module_trace set OFF'
    log_debug_config_message(message)
    msg = debug_log_message_structure()
    log_debug_config_message(msg)
##########################################
def set_log_moduletrace_maxlength(len=40):
    global max_module_trace_length
    max_module_trace_length = len
    set_debug_log_message_format()
    message = 'module_trace_length set to {}'.format(len)
    log_debug_config_message(message)
    msg = debug_log_message_structure()
    log_debug_config_message(msg)
##########################################
def set_log_message_maxlength(len=120):
    global max_message_length
    max_message_length = len
    set_debug_log_message_format()
    message = 'message_length set to {}'.format(len)
    log_debug_config_message(message)
    msg = debug_log_message_structure()
    log_debug_config_message(msg)
##########################################
def set_log_message_maxlinelength(len=160):
    global max_line_length
    max_line_length = len
    set_debug_log_message_format()
    message = 'message_line_length set to {}'.format(len)
    log_debug_config_message(message)
    msg = debug_log_message_structure()
    log_debug_config_message(msg)
##########################################
def set_log_message_display_mode(fmt='FIX-MESSAGE'):
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
    set_debug_log_message_format()
    message = 'message_display_mode set to {}'.format(fmt)
    #log_debug_config_message(message)
    msg = debug_log_message_structure()
    log_debug_config_message(msg)
#####################################################################
def set_log_system_message_prefix(prfix=''):
    global system_message_prefix
    system_message_prefix = prfix
    set_debug_log_message_format()
    message = 'system_message_prefix set to [{}]'.format(prfix)
    log_debug_config_message(message)
##########################################
def set_debug_config_message_prefix(prfix=''):
    global debug_config_message_prefix
    debug_config_message_prefix = prfix
    set_debug_log_message_format()
    message = 'debug_config_message_prefix set to [{}]'.format(prfix)
    log_debug_config_message(message)
##########################################
def set_log_message_prefix(prfix=''):
    global message_prefix
    message_prefix = prfix
    set_debug_log_message_format()
    message = 'message_prefix set to [{}]'.format(prfix)
    log_debug_config_message(message)
    msg = debug_log_message_structure()
    log_debug_config_message(msg)
##########################################
def set_log_message_compress_onoff(onoff='OFF'):
    global message_compressed_enabled 
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        message_compressed_enabled = True
        message = 'message compress set ON'
    else:
        message_compressed_enabled = True
        message = 'message compress set OFF'

    set_debug_log_message_format()
    log_debug_config_message(message)
    msg = debug_log_message_structure()
    log_debug_config_message(msg)

##############shalimar################################
def set_debug_log_message_structure(configString='', max_message_len=0, max_module_trace_len=0, max_line_len=0, message_prefix_string='', message_suffix_string='', offset_chr='', offset_tabs=0):
    global max_message_length
    global max_module_trace_length
    global max_line_length
    global message_display_mode
    global suffix_module
    global prefix_timestamp
    global suffix_timestamp
    global message_prefix
    global message_suffix
    global sessionID
    global UserID
    global suffix
    global prefix
    global sid_prefix
    global sid_suffix
    global uid_prefix
    global uid_suffix
    global message_format
    global offset_enabled
    global offset_char
    global offset_tab
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)

    configString = configString.upper()
    if configString.find('NO-MODULE') >= 0:
        suffix_module = False
    else:
        suffix_module = True

    if configString.find('NO-OFFSET') >= 0:
        offset_enabled = False
    elif configString.find('OFFSET') >= 0:
        offset_enabled = True
    if offset_chr:
        offset_char = offset_chr
    if offset_tabs > 0:
        offset_tab = offset_tabs
        
    prefix_timestamp = False
    suffix_timestamp = False
    if configString.find('TIMESTAMP-PREFIX') >= 0:
        prefix_timestamp = True
    elif configString.find('TIMESTAMP-SUFFIX') >= 0:
        suffix_timestamp = True

    if configString.find('FIX-') >= 0:
        message_display_mode = 'FIX-LINE'
        if configString.find('FIX-MESSAGE') >= 0:
            message_display_mode = 'FIX-MESSAGE'
        elif configString.find('FIX-LINE') >= 0:
            message_display_mode = 'FIX-LINE'
        elif configString.find('FIX-MODULE') >= 0:
            message_display_mode = 'FIX-MODULE'
    else:
        message_display_mode = 'FLOAT'

    if configString.find('SID-PREFIX') >= 0:
        sid_prefix = True
    if configString.find('SID-SUFFIX') >= 0:
        sid_suffix = True
    if configString.find('UID-PREFIX') >= 0:
        uid_prefix = True
    if configString.find('UID-SUFFIX') >= 0:
        uid_suffix = True

    if message_prefix_string:
        message_prefix = message_prefix_string
    if message_suffix_string:
        message_suffix = message_suffix_string

    if max_message_len > 0:
        max_message_length = max_message_len
    if max_module_trace_len > 0:
        max_module_trace_length = max_module_trace_len
    if max_line_len > 0:
        max_line_length = max_line_len
    if max_line_length < 40:
        max_line_length = 40
    if max_message_length > max_line_length - 10:
        max_message_length = max_line_length - 10
    if max_module_trace_length > max_line_length - 10:
        max_module_trace_length = max_line_length - 10
    
    set_debug_log_message_format()
    msg = debug_log_message_structure()
    log_debug_config_message(msg)
###############################################
def set_debug_log_message_format():
    global max_message_length
    global max_module_trace_length
    global max_line_length
    global message_display_mode
    global suffix_module
    global prefix_timestamp
    global suffix_timestamp
    global message_prefix
    global message_suffix
    global sessionID
    global UserID
    global suffix
    global prefix
    global sid_prefix
    global sid_suffix
    global uid_prefix
    global uid_suffix
    global message_format
    global message_format_prefix
    global message_format_suffix
    global offset_enabled
    global offset_char
    global offset_tab
    msgformat_prfx = ''
    if offset_enabled:
        msgformat_prfx = 'OFFSET'
    if sid_prefix:
        msgformat_prfx = msgformat_prfx+' SESSIONID'
    if uid_prefix:
        msgformat_prfx = msgformat_prfx+' USERID'
    if prefix_timestamp:
        msgformat_prfx = msgformat_prfx+' TIMESTAMP'
    msgformat_prfx = msgformat_prfx+' PREFIX'
    message_format_prefix = msgformat_prfx

    msgformat_sfx = 'SUFFIX'
    if sid_suffix:
        msgformat_sfx = msgformat_sfx+' SESSIONID'
    if uid_suffix:
        msgformat_sfx = msgformat_sfx+' USERID'
    if suffix_timestamp:
        msgformat_sfx = msgformat_sfx+' TIMESTAMP'
    if suffix_module:
        msgformat_sfx = msgformat_sfx+' MODULE'
    message_format_suffix = msgformat_sfx

    message_format = message_format_prefix+' MESSAGE '+message_format_suffix

    if max_line_length < 40:
        max_line_length = 40
    if max_message_length > max_line_length - 10:
        max_message_length = max_line_length - 10
    if max_module_trace_length > max_line_length - 10:
        max_module_trace_length = max_line_length - 10
###############################################
def debug_log_message_structure():
    global max_message_length
    global max_module_trace_length
    global max_line_length
    global message_display_mode
    global suffix_module
    global prefix_timestamp
    global suffix_timestamp
    global message_prefix
    global message_suffix
    global sessionID
    global UserID
    global suffix
    global prefix
    global sid_prefix
    global sid_suffix
    global uid_prefix
    global uid_suffix
    global message_format
    global message_format_prefix
    global message_format_suffix
    
    sidprfx = ''
    if sid_prefix:
        sidprfx = 'SID'
    uidprfx = ''
    if uid_prefix:
        uidprfx = 'UID'
    timprfx = ''
    if prefix_timestamp:
        timprfx = 'TIMESTAMP'

    sidsfx = ''
    if sid_prefix:
        sidsfx = 'SID'
    uidsfx = ''
    if uid_prefix:
        uidsfx = 'UID'
    modsfx = ''
    if suffix_module:
        modsfx = 'MODULE'
    timsfx = ''
    if suffix_timestamp:
        timsfx = 'TIMESTAMP'

    message = 'debug_log_message:{}({},{},{}),'.format(message_display_mode, max_line_length,max_message_length, max_module_trace_length)
    # message = '{} suffix["{}" {} {} {} {}],'.format(message, message_suffix, timsfx, modsfx, sidsfx, uidsfx)
    # message = '{} prefix[{} {} {} "{}"]'.format(message, timprfx, sidprfx, uidprfx, message_prefix)
    message = '{} format[{}]'.format(message, message_format)
    return message
#-------------------------------------------------------------------------
##########################################
##########################################
##########################################
### config functions                   ###
##########################################
##########################################
##########################################
def set_global_debug(onoff='ON'):
    global global_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    message = ''
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        if not global_debug_enabled:
            global_debug_enabled = True
            message = 'global debug set ON'
    else:
        if global_debug_enabled:
            global_debug_enabled = False
            message = 'global debug set OFF'
    if message:
        log_debug_config_message(message)
##########################################
def set_debug_defaults(onoff='ON', debuglevel=9):
    global default_debug_onoff
    global default_debug_level
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    message = ''
    debugonoff = False
    default_debug_onoff_Str = 'OFF'
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        debugonoff = True
        default_debug_onoff_Str = 'ON'
    if default_debug_level != debuglevel or default_debug_onoff != debugonoff:
        default_debug_level = debuglevel
        default_debug_onoff = debugonoff
        message = 'log debug defaults set to {} level {}.'.format(default_debug_onoff_Str, default_debug_level)
    if message:
        log_debug_config_message(message)
##########################################
def set_debug_config_message_ONOFF(onoff='OFF', silent=False):
    global debug_config_message_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    message = ''
    if onoff in ['ON', 1, '1', 'YES', 'Y', True]:
        thisval = True
        msg = 'debug config messaging set ON'
    else:
        thisval = False
        msg = 'debug config messaging set OFF'
    if debug_config_message_enabled != thisval:
        debug_config_message_enabled = thisval
        message = msg
    if not silent:
        log_debug_config_message(message)
##########################################
##########################################
##########################################
### modules config                     ###
##########################################
##########################################
##########################################
def set_module_debug_off(module_name):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    set_debug_level(module=module_name, component='', priority=1, debugOnOff='OFF')
    message = 'log debug set OFF for module {}'.format(module_name)
    log_info(message)
##########################################
def set_module_debug_on(module_name):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    set_debug_level(module=module_name, component='', priority=1, debugOnOff='ON')
    message = 'log debug set ON for module {}'.format(module_name)
    log_info(message)
##########################################
def set_module_debug_level(module_name='', debug_level=9):
    global active_component_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
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
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    set_debug_level(module=module_name, component=component_name, priority=2, debugOnOff='OFF')
    message = 'log debug set OFF for component {}.{}'.format(module_name, component_name)
    log_info(message)
##########################################
def set_component_debug_on(component_name='', module_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    set_debug_level(module=module_name, component=component_name, priority=2, debugOnOff='ON')
    message = 'log debug set ON for component {}.{}'.format(module_name, component_name)
    log_info(message)
##########################################
def set_component_debug_level(component_name='', debug_level=9, module_name=''):
    global active_component_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
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
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    set_debug_level(module=module_name, component=component_name, component_type=component_type, priority=3, debugOnOff='OFF')
    message = 'log debug set OFF for component type {}.{}.{}'.format(module_name, component_name,component_type)
    log_info(message)
##########################################
def set_componenttype_debug_on(component_type='', component_name='', module_name=''):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    set_debug_level(module=module_name, component=component_name, component_type=component_type, priority=3, debugOnOff='ON')
    message = 'log debug set ON for component type {}.{}.{}'.format(module_name, component_name,component_type)
    log_info(message)
##########################################
def set_componenttype_debug_level(component_type='', component_name='', debug_level=9, module_name=''):
    global active_component_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    retrieve_activecomponent_debug_info(module_name=module_name, component_name=component_name, component_type=component_type)
    onoff = 'OFF'
    if active_component_debug_enabled:
        onoff = 'ON'
    retrieve_activecomponent_debug_info()
    set_debug_level(module=module_name, component=component_name, component_type=component_type, priority=3, debugOnOff=onoff, debugLevel=debug_level)
    message = 'log debug level set to {}-{} for component type {}.{}.{}'.format(onoff, debug_level, module_name, component_name, component_type)
    log_info(message)
##########################################
def set_debug_log_services_level(lev='WARNING'): #WARNING , ERROR, INFO, BEGIN-END VARIABLE PARAMETER URL
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    lev = lev.upper()
    debug_log_services_level = lev
    message = 'debug_log_services_level set to {}'.format(debug_log_services_level)
    log_debug_config_message(message)
##########################################
def set_debug_log_services_level_remove(lev='WARNING'):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    lev = lev.upper()
    debug_log_services_level = debug_log_services_level.replace(lev,'')
    message = 'debug_log_services_level set to {}'.format(debug_log_services_level)
    log_debug_config_message(message)
##########################################
def set_debug_log_services_level_add(lev='WARNING'):
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    lev = lev.upper()
    if debug_log_services_level.find(lev) < 0:
        debug_log_services_level = debug_log_services_level + ';' + lev
    message = 'debug_log_services_level set to {}'.format(debug_log_services_level)
    log_debug_config_message(message)
##########################################
def config_from_environment_variables(silent=False):
    global debug_config_message_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)
    prevstate = debug_config_message_enabled
    debug_config_message_enabled = True
    if silent:
        debug_config_message_enabled = False
    
    config_message_ONOFF = ""
    for item in os.environ:
        if item.upper().find('DEBUG_') == 0:
            what = item.upper().replace('DEBUG_', '').lower()
            val = os.environ.get(item).upper()
            # if what.find('incl') >= 0:
            #     print('xxxxxxxx')
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
            elif what.upper().find('DEBUGLOGSERVICES') == 0:
                config_message_ONOFF = valonoff
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

    debug_config_message_enabled = prevstate
    if config_message_ONOFF:
        set_debug_config_message_ONOFF(config_message_ONOFF)
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
    set_debug_log_message_format()
    message = 'log debug module set to ({})'.format(thisModule)
    log_debug_config_message(message)
    components_stack = {}
    #print('terminal colors test:')
    ColorsInit(convert=True)
    # print(Fore.WHITE)
    # print('Fore.WHITE')
    # print(Back.BLACK)
    # print('Back.BLACK')
    # print(Fore.RED + 'some red text') 
    # print(Back.GREEN + 'and with a green background') 
    # print(Style.DIM + 'and in dim text') 
    # print(Fore.WHITE)
    # print('Fore.WHITE')
    # print(Back.BLACK)
    # print('Back.BLACK')
    # print(Style.RESET_ALL) 
    # print('back to normal now') 
    # print(Fore.WHITE)
    # print('Fore.WHITE')
    # print(Back.BLACK)
    # print('Back.BLACK')

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
    global debug_config_message_enabled
    global active_component_debug_enabled
    xcaller = sys._getframe(1)  # Obtain calling frame
    tispaolas(xcaller)

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
        set_global_debug('ON')
        set_debug_defaults(onoff='OFF', debuglevel=9)
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
        log_debug_config_message(message)

    message = 'debug levels for folder "{}" module "{}" component "{}" compo-type "{}" set to ({}-{}) priority {}.'.format(folder, module, component, component_type, debugOnOff_Str, debugLevel, CalculatedPriority)
    log_debug_config_message(message)
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
    global activeKey
    global prevKey
    global active_chain

    if not global_debug_enabled:
        active_component_debug_enabled = False
        active_component_debug_level = 0
        #print ('===global_debug_enabled is OFF')
        return
    #print('### active_module is [', active_module, ']')
    # activeKey = module_name+'.'+component_name+'.'+component_type
    # print('### 1-search for [', activeKey, ']')

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
    activeKeyStr = '['+module_name+']['+component_name+']['+component_type+']'
    active_chain = component_type + ':' + module_name + '.' + component_name
    print_enabled = False
    if active_chain.lower().find('xadministration') >= 0:
        print_enabled = True
    if print_enabled:
        print('')
        print('===SEARCH FOR:', activeKeyStr)
    found = False
    for ix, moduleArray in enumerate(Components):
        module = moduleArray[0]
        if print_enabled:
            print(ix, '===SEARCH FOR:', activeKeyStr)
            print(ix, 'key', module)
            print (ix, 'folder',folder_name,'<--',moduleArray[5])
            print (ix, 'module',module_name,'<--',moduleArray[6])
            print (ix, 'component',component_name,'<--',moduleArray[7])
            print (ix, 'type',component_type,'<--',moduleArray[8])
        priority = moduleArray[1]
        onoffStr = moduleArray[2]
        onoff = moduleArray[3]
        debuglevel = moduleArray[4]
        match = False
        px = ''
        # if print_enabled:
        #     x="1 {} == {} or {} in ('', '*')".format(module_name,moduleArray[6],moduleArray[6])
        #     print(x, '-->', module_name == moduleArray[6] or moduleArray[6] in ('', '*'))
        #     x="2 {} find({})".format(str('.'+module_name+'.'),str('.'+moduleArray[6]+'.'))
        #     print(x, '-->', str('.'+module_name+'.').find(str('.'+moduleArray[6]+'.')))
        #     x="3 {} find({})".format(str('.'+moduleArray[6]+'.'),str('.'+module_name+'.'))
        #     print(x, '-->', str('.'+moduleArray[6]+'.').find(str('.'+module_name+'.')))
        #     x="4 {} == {} or {} in ('', '*')".format(component_name, moduleArray[7], moduleArray[7])
        #     print(x, '-->', component_name == moduleArray[7] or moduleArray[7] in ('', '*'))
        #     x="5 {} == {} or {} in ('', '*')".format(component_type, moduleArray[8] , moduleArray[8])
        #     print(x, '-->', component_type == moduleArray[8] or moduleArray[8] in ('', '*'))
        if folder_name == moduleArray[5] or moduleArray[5] in ('', '*'):
            if module_name == moduleArray[6] or moduleArray[6] in ('', '*') \
            or str('.'+module_name+'.').find(str('.'+moduleArray[6]+'.')) >= 0 \
            or str('.'+module_name+'.').find(str(moduleArray[6]+'.')) >= 0 \
            or str('.'+module_name+'.').find(str('.'+moduleArray[6])) >= 0 \
            or str('.' + moduleArray[6] + '.').find(str('.' + module_name + '.')) >= 0:
                if component_name == moduleArray[7] or moduleArray[7] in ('', '*'):
                    if component_type == moduleArray[8] or moduleArray[8] in ('', '*'):
                        match = True
        #print('--------------------------------------')
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
            active_component_debug_enabled = onoff
            active_component_debug_level = debuglevel
            if print_enabled:
                print ('===FOUND', ix, activeKey, '-->', module, 'MATCHED', onoff, debuglevel)
            break
        #else:
            #print ('xxxx', activeKey, i, module, 'NOT MATCHED')
    if not found:
        active_component_debug_enabled = default_debug_onoff
        active_component_debug_level = default_debug_level
        if print_enabled:
            print('===NOT-FOUND', activeKey, active_component_debug_enabled, active_component_debug_level)
    if print_enabled:
        print('')
#############################################################
def smart_fixlength_string(msg='?', msgfixlength=80, direction='LEFT-TO-RIGHT'):
    direction = direction.upper().replace('_', '-').replace(' ', '-')
    if direction == 'LEFT-TO-RIGHT':
        actual_msg_len = len(msg)
        if actual_msg_len > msgfixlength:
            msg = msg[:msgfixlength - 3]+'...' #truncate upto msgfixlength-3 + ...
        #msg = msg.ljust(msgfixlength-1)+'>' #right pad with spaces upto msgfixlength + ...
        msg = msg + ' '* 640
        msg = msg[:msgfixlength] #truncate upto msgfixlength + ...
        return msg
    else:
        #direction.upper() == 'RIGHT-TO-LEFT':
        actual_msg_len = len(msg)
        if actual_msg_len > msgfixlength:
            ofs = (actual_msg_len - msgfixlength) + 3 
            msg = '...' + msg[ofs:]
        msg = msg[:msgfixlength] #truncate upto msgfixlength + ...
        return msg

################################################################################

################################################################################

def combined_message(msg='?', p1='', p2='', p3='', p4='', p5=''):
    message = msg
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
    return message

def formatted_message(msg='?', p1='', p2='', p3='', p4='', p5='', msgtype='', Nocolors=False):
    global offset
    global active_module
    global activeKey
    global active_chain
    global system_message_prefix
    global message_format
    global message_format_prefix
    global message_format_suffix
    global max_message_length
    global max_module_trace_length
    global max_line_length
    global message_display_mode
    global suffix_module
    global prefix_timestamp
    global suffix_timestamp
    global message_prefix
    global message_suffix
    global sessionID
    global UserID
    #global suffix
    #global prefix
    global sid_prefix
    global sid_suffix
    global uid_prefix
    global uid_suffix
    global active_color

    # if active_level >= 0:
    #     col = component_color(active_level)
    # else:
    #     col = fore.WHITE

    #message = '{}{}{}'.format(message_prefix, offset, msg)
    message = msg
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
    
    global message_format
    global message_format_prefix
    global message_format_suffix

    msg0 = ' ' + message_format_prefix.upper()
    msg1 = msg0.replace(' OFFSET', offset.replace('>', offset_char))
    msg2 = msg1.replace(' PREFIX', message_prefix)
    msg3 = msg2.replace(' SUFFIX', message_suffix)
    msg4 = msg3.replace(' TIMESTAMP', datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    msg5 = msg4.replace(' SESSIONID', sessionID)
    msg6 = msg5.replace(' USERID', UserID)
    msgprfx = msg6.lstrip()

    msg0 = ' '+message_format_suffix.upper()
    msg1 = msg0.replace(' OFFSET', offset.replace('>',offset_char))
    msg2 = msg1.replace(' PREFIX', message_prefix)
    msg3 = msg2.replace(' SUFFIX', message_suffix)
    msg4 = msg3.replace(' TIMESTAMP', datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    msg5 = msg4.replace(' SESSIONID', sessionID)
    msg6 = msg5.replace(' USERID', UserID)
    msg7 = msg6.replace(' MODULE', active_module)
    msgsfx = msg7.lstrip()

    # if msgtype.upper() = 'WARNING':
    #     msgtype = 'warning:'

    msg7 = msg6.replace('MESSAGE', message)
    #PREFIX TIMESTAMP MODULE o MESSAGE TIMESTAMP MODULE SUFFIX SID UID'
    #message = '{}{}{}'.format(message_prefix, offset, msg)
    if msgtype.upper().find('START') >= 0 or msgtype.upper().find('FINISH') >= 0:
        msg8 = '{}{} [{}]'.format(msgprfx, message, active_chain)
        if not Nocolors:    
            msg8 = '{}{}{}'.format(active_color, msg8, Style.RESET_ALL)
        return msg8
    else:
        msg8 = '{}{}'.format(msgprfx, message)

    message = msg8

    if not suffix_module:
        if message_display_mode.upper().find('FIX') >=0 :
            formatted_message = message[:max_line_length] 
        else:
            formatted_message = message
    else:
        if message_display_mode.upper() == 'FIX-MESSAGE':
            #method 1 fix-message-length
            msg = smart_fixlength_string(message, max_message_length, 'LEFT-TO-RIGHT')
            module_length = max_line_length - max_message_length - 2 - 1
            mod = smart_fixlength_string(msgsfx, module_length, 'RIGHT-TO-LEFT')
            formatted_message = '{} [{}]'.format(msg, mod)
            formatted_message = formatted_message[0:(max_line_length)]
        elif message_display_mode.upper() == 'FIX-MODULE':
            #method 2: fix-module-position
            mod = smart_fixlength_string(msgsfx, max_module_trace_length, 'RIGHT-TO-LEFT')
            msg_length = max_line_length - max_module_trace_length - 2 - 1
            msg = smart_fixlength_string(message, msg_length, 'LEFT-TO-RIGHT')
            formatted_message = '{} [{}]'.format(msg, mod)
            formatted_message = formatted_message[:max_line_length]
        elif message_display_mode.upper() == 'FIX-LINE':
            #method 3: fix-line-length
            if max_line_length < (len(message) + len(msgsfx) + 2 + 1):
                module_length = max_line_length - len(message) - 2 -1
                if module_length > 0:
                    mod = smart_fixlength_string(msgsfx, module_length, 'RIGHT-TO-LEFT')
                else:
                    mod = ''
                msg = smart_fixlength_string(message, len(message), 'LEFT-TO-RIGHT')
                msg = '{} [{}]'.format(msg, mod)
                formatted_message = msg
            else:
                msg_length = max_line_length - len(msgsfx) - 2 - 1
                msg = smart_fixlength_string(message, msg_length, 'LEFT-TO-RIGHT')
                formatted_message = '{} [{}]'.format(msg, msgsfx)
            formatted_message = formatted_message[:max_line_length]
        elif message_display_mode.upper() == 'AUTO':
            formatted_message = message[:max_line_length]
        else:
            #method 3: floating msg (full)
            formatted_message = '{} [{}]'.format(message, msgsfx)
    if not Nocolors:    
        formatted_message = '{}{}{}'.format(active_color, formatted_message, Style.RESET_ALL)
    return formatted_message
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
def component_color(clevel):
    lev = clevel - 8*int(clevel / 8)
    if lev == 0:
        col = Fore.CYAN
    elif lev == 1:
        col = Fore.BLUE
    elif lev == 2:
        col = Fore.MAGENTA
    elif lev == 3:
        col = Fore.YELLOW
    elif lev == 4:
        col = Fore.GREEN
    elif lev == 5:
        col = Fore.LIGHTBLUE_EX
    elif lev == 6:
        col = Fore.LIGHTMAGENTA_EX
    elif lev == 7:
        col = Fore.LIGHTGREEN_EX
    else:
        col = Fore.LIGHTRED_EX
    return col
# #BLACK:'\x1b[30m'
# #BLUE:'\x1b[34m'
# #CYAN:'\x1b[36m'
# #GREEN:'\x1b[32m'
# LIGHTBLACK_EX:'\x1b[90m'
# LIGHTBLUE_EX:'\x1b[94m'
# LIGHTCYAN_EX:'\x1b[96m'
# LIGHTGREEN_EX:'\x1b[92m'
# LIGHTMAGENTA_EX:'\x1b[95m'
# LIGHTRED_EX:'\x1b[91m'
# LIGHTWHITE_EX:'\x1b[97m'
# LIGHTYELLOW_EX:'\x1b[93m'
# #MAGENTA:'\x1b[35m'
# RED:'\x1b[31m'
# RESET:'\x1b[39m'
# WHITE:'\x1b[37m'
# #YELLOW: '\x1b[33m'
    


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
if __name__ == '__main__':
    #tests
    #global Components
    x = smart_fixlength_string(msg='12345678901234567890', msgfixlength=11, direction='LEFT-TO-RIGHT')
    print (x)
    x = smart_fixlength_string(msg='1234567890123456789X', msgfixlength=11, direction='RIGHT-TO-LEFT')
    print (x)

    # set_debug_defaults(onoff='ON', debuglevel=9)
    # set_debug_level(module='webapp', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='external_services', debugOnOff='OFF', debugLevel=9)
    # set_debug_level(module='*', component='geolocation_services', priority=88, debugOnOff='OFF', debugLevel=1)
    # set_debug_level(module='*', component='geolocation_services', component_type='view' , priority=89, debugOnOff='OFF', debugLevel=2)
    # set_debug_level(module='*', component='log_services', priority=88, debugOnOff='ON', debugLevel=9)
    # #print (Components)
    # # i = 0
    # # for x in Components:
    # #     i=i+1
    # #     print(i,x)
    # active_module = 'a.b.geolocatioxn_services'
    # retrieve_activecomponent_debug_info('view')
    # print('result:', active_module, active_component_debug_enabled, active_component_debug_level)
    # testx()
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

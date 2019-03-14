import sys
from datetime import datetime
level = 0
offset = ''
trailer = ''
modules_stack = {}
modules_NoDebug = {}
active_module = ''
offset_char = '.'
offset_tab = 3
sessionID = ''
UserID = ''
prefix = ''
suffix = ''
prefix_timestamp = False
suffix_timestamp = False
active_moduleX = ''
##########################################
def log_info(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    if active_module_debug_is_on():
        message = '{0}{1} {2} {3} {4} {5} {6} [{7}]'.format(offset, msg, m1, m2, m3, m4, m5, active_moduleX)
        print(message)
##########################################
def log_error(msg, m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    if active_module_debug_is_on():
        #caller = sys._getframe(1)  # Obtain calling frame
        #caller = inspect.currentframe().f_back
        #print("Called from module", caller.f_globals['__name__'])
        #print(offset+'ERROR:'+msg , caller.f_globals['__name__'], m1, m2 ,m3 ,m4, m5, trailer)
        message = '{0}ERROR:{1} {2} [{3}] {4} {5} {6} {7}'.format(offset, msg, m1, active_moduleX, m2, m3, m4, m5)
        print(message)
##########################################
def log_variable(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    if active_module_debug_is_on():
        msg = '{0}={1}'.format(name, value)
        message = '{0}{1} {2} {3} {4} {5} {6} [{7}]'.format(offset, msg, m1, m2, m3, m4, m5, active_moduleX)
        print(message)
##########################################
def log_variable_short(name='', value='', m1='', m2='', m3='', m4='', m5=''):
    global offset
    global trailer
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    if active_module_debug_is_on():
        valueStr = str(value)
        if len(valueStr)>37:
            valueStr = valueStr[0:37] + '...' 
        msg = '{0}={1}'.format(name, valueStr)
        message = '{0}{1} {2} {3} {4} {5} {6} [{7}]'.format(offset, msg, m1, m2, m3, m4, m5, active_moduleX)
        print(message)
##########################################
def log_url_param(name='', value=''):
    global offset
    global trailer
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    if active_module_debug_is_on():
        msg = '{0}={1} [{3}]'.format(name, value, active_moduleX)
        print(offset+'url-param', msg, trailer)
##########################################
def log_module_start(module_name=''):
    global offset
    global level
    global modules_stack
    global trailer
    global active_module
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    active_module = module_name
    if active_module_debug_is_on():
        print(offset+'start', '['+module_name+']', active_moduleX)
    level = level + 1
    modules_stack.update({level : module_name})
    offset = set_offset(level)
##########################################
def log_module_finish(module_name=''):
    global offset
    global level
    global modules_stack
    global trailer
    global active_module
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    maxlev = -1
    maxmodule = '?'
    lev = -1
    for x in modules_stack.items():
        maxlev = x[0]
        maxmodule = x[1]
        #print('==',x[0],x[1],module_name)
        if x[1] == module_name:
            lev = x[0]
    if lev == -1:
        lev = maxlev
        module_name = maxmodule
    offset = set_offset(lev-1)
    caller = sys._getframe(1)  # Obtain calling frame
    if active_module_debug_is_on():
        print(offset+'finish', '['+module_name+']', active_moduleX)
   
    rem = 0
    for x in modules_stack.items():
        if x[0] >= lev:
            rem = rem +1
            #modules_stack.pop(x[0])
        else:        
            level = x[0]

    #print('rem',rem,level)
    i = 1
    while i <= rem:
        modules_stack.popitem()    
        i = i + 1

    level = 0
    for x in modules_stack.items():
        level = x[0]
        active_module = x[1]
    offset = set_offset(level)
##########################################
def set_log_prefix(sid, uid):
    global sessionID
    global UserID
    global prefix
    global level
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    global offset

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
    set_offset(level)
    if active_module_debug_is_on():
        message = '***log_prefix set to {} [{}]'.format(prefix,active_moduleX)
        print(message)
##########################################
def set_log_suffix(sid, uid):
    global sessionID
    global UserID
    global suffix
    global level
    global level
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    global offset

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
    set_offset(level)
    if active_module_debug_is_on():
        message = '***log_suffix set to {} [{}]'.format(suffix,active_moduleX)
        print(message)
##########################################
def set_log_suffix_timestamp(o=1):
    global suffix_timestamp
    global level
    global level
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    global offset

    suffix_timestamp = False
    OnOff = "OFF"
    if o in [1, '1', 'YES', 'Y', True]:
        suffix_timestamp = True
        OnOff = "ON"
    set_offset(level)
    if active_module_debug_is_on():
        message = '***log_suffix_timestamp {} [{}]'.format(OnOff, active_moduleX)
        print(message)
##########################################
def set_log_prefix_timestamp(o=1):
    global prefix_timestamp
    global level
    global level
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    global offset

    prefix_timestamp = False
    OnOff = "OFF"
    if o in [1, '1', 'YES', 'Y', True]:
        prefix_timestamp = True
        OnOff = "ON"
    set_offset(level)
    if active_module_debug_is_on():
        message = '***log_prefix_timestamp {} [{}]'.format(OnOff, active_moduleX)
        print(message)
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

def set_debug_off(module_name):
    global modules_NoDebug 
    global level
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    global offset

    modules_NoDebug.update({module_name:'OFF'})
    if active_module_debug_is_on():
        message = '***log debug set OFF for {} [{}]'.format(module_name, active_moduleX)
        print(message)

def set_debug_on(module_name):
    global modules_NoDebug 
    global level
    global active_moduleX
    caller = sys._getframe(1)  # Obtain calling frame
    active_moduleX = caller.f_globals['__name__']
    global offset

    modules_NoDebug.update({module_name:'ON'})
    if active_module_debug_is_on():
        message = '***log debug set ON for {} [{}]'.format(module_name, active_moduleX)
        print(message)

def module_debug_is_on(module=''):
    global modules_NoDebug 
    if modules_NoDebug.get(module) == 'OFF':
        return False
    else:
        return True

def active_module_debug_is_on():
    global active_module
    global active_moduleX
    modules = active_moduleX.split(".")
    modules.append(active_module)
    modules.append(active_moduleX)
    #print(modules)
    off = False
    i = 0
    for module in modules:
        i = i+1
        if not module_debug_is_on(module):
            off = True
    return not(off )
##########################################
if __name__ == '__main__':
    set_log_prefix_timestamp(1)
    set_log_prefix('SID-2','US01')
    log_module_start('alpha')
    log_info('test alpha.....')
    log_variable('var', 'alpha')
    log_module_start('beta')
    log_variable('var', 'beta')
    log_module_start('gama')
    log_variable('var', 'gama')
    log_module_finish('gama')
    log_variable('var', 'beta')
    log_module_finish('beta')
    log_variable('var', 'alpha')
    log_module_finish('alpha')
    log_variable('test', 'test')

    set_log_prefix_timestamp(0)
    set_log_prefix('','')
    set_log_suffix_timestamp(1)
    #set_log_suffix('SID-x','xxx1')

    log_module_start('alpha')
    log_info('test alpha.....')
    log_variable('var', 'alpha')
    log_module_start('beta')
    log_variable('var', 'beta')
    log_module_start('gama')
    log_variable('var', 'gama')
    log_module_finish('gama')
    log_variable('var', 'beta')
    log_module_finish('beta')
    log_variable('var', 'alpha')
    log_module_finish('alpha')
    log_variable('test', 'test')

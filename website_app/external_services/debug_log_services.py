import sys
from datetime import datetime
level = 0
offset = ''
trailer = ''
modules_stack = {}
offset_char = '.'
offset_tab = 3
sessionID = ''
UserID = ''
prefix = ''
suffix = ''
prefix_timestamp = False
suffix_timestamp = False
##########################################
def log_info(msg, m1='', m2='', m3=''):
    global offset
    caller = sys._getframe(1)  # Obtain calling frame
    print(offset+msg ,m1 ,m2 ,m3 ,caller.f_globals['__name__'])
##########################################
def log_error(msg, m1='', m2='', m3=''):
    global offset
    caller = sys._getframe(1)  # Obtain calling frame
    #caller = inspect.currentframe().f_back
    #print("Called from module", caller.f_globals['__name__'])
    print(offset+'ERROR:'+msg , caller.f_globals['__name__'], m1, m2 ,m3 ,trailer)
##########################################
def log_variable(name='', value='', m1='', m2='', m3=''):
    global offset
    msg = '{0}={1}'.format(name, value)
    caller = sys._getframe(1)  # Obtain calling frame
    print(offset+msg, m1 ,m2 ,m3 ,caller.f_globals['__name__'])
##########################################
def log_url_param(name='', value=''):
    global offset
    msg = '{0}={1}'.format(name, value)
    print(offset+'url-param', msg, trailer)
##########################################
def log_module_start(module_name=''):
    global offset
    global level
    global modules_stack
    global trailer
    caller = sys._getframe(1)  # Obtain calling frame
    print(offset+'start', module_name, caller.f_globals['__name__'])
    level = level + 1
    modules_stack.update({level : module_name})
    offset = set_offset(level)
##########################################
def log_module_finish(module_name=''):
    global offset
    global level
    global modules_stack
    global trailer
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
    print(offset+'finish', module_name,caller.f_globals['__name__'])
   
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
    offset = set_offset(level)
##########################################
def set_log_prefix(sid, uid):
    global sessionID
    global UserID
    global prefix
    global level
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
##########################################
def set_log_suffix(sid, uid):
    global sessionID
    global UserID
    global suffix
    global level
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
##########################################
def set_log_suffix_timestamp(o=1):
    global suffix_timestamp
    global level
    suffix_timestamp = False
    if o in [1, '1', 'YES', 'Y', True]:
        suffix_timestamp = True
    set_offset(level)
##########################################
def set_log_prefix_timestamp(o=1):
    global prefix_timestamp
    global level
    prefix_timestamp = False
    if o in [1, '1', 'YES', 'Y', True]:
        prefix_timestamp = True
    set_offset(level)
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

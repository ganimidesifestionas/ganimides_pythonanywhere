import os
import sys
from pathlib import Path
def add_to_sys_path(fromthisfile=__file__):
    print('*** o system)services from ', __file__)
    x = find_folder_in_chain('static', root_folder='')
    if x:
        application_folder = os.path.abspath(os.path.dirname(x))
        project_folder = os.path.abspath(os.path.dirname(application_folder))
    else:
        application_folder = os.path.abspath(os.path.dirname(__file__))
        project_folder = os.path.abspath(os.path.dirname(application_folder))
    print('*** o application_folder = ', application_folder)
    print('*** o project_folder = ', project_folder)

    x = find_folder_in_chain('external_services', project_folder)
    if x:
        external_services_folder = x
    else:
        external_services_folder = os.path.abspath(os.path.dirname(__file__))
    print('*** o external_services_folder = ', external_services_folder)

    x = find_folder_in_chain('debug_services', project_folder)
    if x:
        debug_services_folder = x
    else:
        debug_services_folder = os.path.abspath(os.path.dirname(__file__))
    print('*** o debug_services_folder = ', debug_services_folder)

    if external_services_folder not in sys.path:
        sys.path.append(str(external_services_folder))
        print('*** ooo system_services-add_to_sys_path:{}'.format(external_services_folder))
    else:
        print('*** ooo system_services-add_to_sys_path: external_services_folder already in sys.path')

    if debug_services_folder not in sys.path:
        sys.path.append(str(debug_services_folder))
        print('*** ooo system_services-add_to_sys_path:{}'.format(debug_services_folder))
    else:
        print('*** ooo system_services-add_to_sys_path: debug_services_folder already in sys.path')

    if application_folder not in sys.path:
        sys.path.append(str(application_folder))
        print('*** ooo system_services-add_to_sys_path:{}'.format(application_folder))
    else:
        print('*** ooo system_services-add_to_sys_path: application_folder already in sys.path')

    if project_folder not in sys.path:
        sys.path.append(str(project_folder))
        print('*** ooo system_services-add_to_sys_path:{}'.format(project_folder))
    else:
        print('*** ooo system_services-add_to_sys_path: project_folder already in sys.path')

def find_folder_in_chain(target_foldername='external_services', root_folder=''):
    if os.path.isdir(root_folder):
        parent_folder = root_folder
    else:
        if os.path.isfile(root_folder):
            parent_folder = os.path.abspath(os.path.dirname(root_folder))
        else:
            parent_folder = os.path.abspath(os.path.dirname(__file__))
    root_folder = parent_folder
    prev_parent_folder = '*'
    parent_folder = root_folder  
    target_folder = os.path.join(parent_folder, target_foldername)
    ix = 0
    #print(ix, target_folder)
    while not os.path.isdir(target_folder) and ix <= 100 and parent_folder != prev_parent_folder:
        ix = ix + 1
        prev_parent_folder = parent_folder
        parent_folder = os.path.abspath(os.path.dirname(parent_folder))
        target_folder = os.path.join(parent_folder, target_foldername)
        #print(ix, target_folder)
    if os.path.isdir(target_folder):
        #print('o {} FOUND in upper chain...{}'.format(target_foldername, target_folder))
        return target_folder
    else:
        target_folder = ''
        path = root_folder
        #print(path)
        ix = 0
        found = False
        for root, dirs, files in os.walk(path):
            if target_foldername in dirs:
                target_folder = os.path.join(root, target_foldername)
                #print('found...', os.path.join(root, target_foldername))
                found = True
                break
        if os.path.isdir(target_folder):
            #print('o {} FOUND in chain...{}'.format(target_foldername, target_folder))
            return target_folder
        else:
            #print('o {} NOT FOUND in chain...{}'.format(target_foldername, target_folder))
            return ''
#under dev
def find_file_in_chain(target_foldername='server.ini', root_folder=''):
    parent_folder = os.path.abspath(os.path.dirname(__file__))
    root_folder = parent_folder
    prev_parent_folder = '*'
    parent_folder = root_folder  
    target_folder = os.path.join(parent_folder, target_foldername)
    ix = 0
    #print(ix, target_folder)
    while not os.path.isdir(target_folder) and ix <= 100 and parent_folder != prev_parent_folder:
        ix = ix + 1
        prev_parent_folder = parent_folder
        parent_folder = os.path.abspath(os.path.dirname(parent_folder))
        target_folder = os.path.join(parent_folder, target_foldername)
        #print(ix, target_folder)
    if os.path.isdir(target_folder):
        #print('o {} FOUND in upper chain...{}'.format(target_foldername, target_folder))
        return target_folder
    else:
        target_folder = ''
        path = root_folder
        #print(path)
        ix = 0
        found = False
        for root, dirs, files in os.walk(path):
            if target_foldername in dirs:
                target_folder = os.path.join(root, target_foldername)
                #print('found...', os.path.join(root, target_foldername))
                found = True
                break
        if os.path.isdir(target_folder):
            #print('o {} FOUND in chain...{}'.format(target_foldername, target_folder))
            return target_folder
        else:
            #print('o {} NOT FOUND in chain...{}'.format(target_foldername, target_folder))
            return ''
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# init
# # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # 
add_to_sys_path(fromthisfile=__file__)
# # # # # # # # # # # # # # # # # # # # # # # # # # 

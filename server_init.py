"""
This script configures server parameters from server.ini
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import os.path
from os import environ
import configparser
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
ServerDictionary = {}
EnvServerKeys = []
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def initialize_server(startupProgram_fullpathfile='', server_ini_filename='server.ini', debug=False, print_env_params=False, print_all_env_params=False):
    global ServerDictionary
    global EnvServerKeys
    print('...start: server.ini')
    if not startupProgram_fullpathfile:
        startupProgram_fullpathfile = __file__
    thisfile = os.path.abspath(startupProgram_fullpathfile)
    thisDir = os.path.dirname(startupProgram_fullpathfile)
    thisFileName = os.path.basename(startupProgram_fullpathfile)
    exec_folder = os.path.abspath(os.path.dirname(startupProgram_fullpathfile))
    server_config_folder = os.path.dirname(exec_folder)
    server_ini_filename = server_ini_filename  # 'server.ini'
    server_config_filename = 'server_config.py'
    server_ini_file = os.path.join(server_config_folder, server_ini_filename)
    server_config_file = os.path.join(server_config_folder, server_config_filename)
    server_relative_config_path = "..\\"  # relative to instance

    # find the server.ini file in a folder up to the current
    prev_config_folder = '*'
    config_folder = os.path.abspath(os.path.dirname(startupProgram_fullpathfile))
    ini_file = os.path.join(config_folder, server_ini_filename)
    ix = 0
    #print(ix, config_folder)
    #print(ix, ini_file)
    while not os.path.isfile(ini_file) and ix <= 100 and config_folder != prev_config_folder:
        ix = ix + 1
        prev_config_folder = config_folder
        config_folder = os.path.abspath(os.path.dirname(config_folder))
        ini_file = os.path.join(config_folder, server_ini_filename)
        #print(ix, config_folder)
        #print(ix, ini_file)
    if os.path.isfile(ini_file):
        server_ini_file = ini_file
        server_config_folder = config_folder
        if debug:
            print('......server_ini_file FOUND in chain...', server_ini_file)

    if debug:
        print('......Server_Startup_Program =', __file__)
        print('......Server_Startup_Folder =', thisDir)
        print('......Server_Startup_ProgramName =', thisFileName)
        print('......Server_Exec_Folder =', exec_folder)
        print('......Server_Config_Folder =', server_config_folder)
        print('......server_ini_file =', server_ini_file)
        print('......server_config_file =', server_config_file)
        print('......server_ini_file_name =', server_ini_filename)
        print('......server_config_file_name =', server_config_filename)
        print('......server_relative_config_path =', server_relative_config_path)
    ################################################################
    ServerDictionary.update({'Server_Startup_Program': startupProgram_fullpathfile})
    ServerDictionary.update({'Server_Startup_Folder': thisDir})
    ServerDictionary.update({'Server_Startup_Program_Name': thisFileName})
    ServerDictionary.update({'Server_Startup_Execfolder': exec_folder})
    ServerDictionary.update({'Server_Config_Folder': server_config_folder})
    ServerDictionary.update({'server_ini_file_Name': server_ini_filename})
    ServerDictionary.update({'server_config_file_Name': server_config_filename})
    ServerDictionary.update({'server_ini_file': server_ini_file})
    ServerDictionary.update({'server_relative_config_path': server_relative_config_path})
    for serveritem in ServerDictionary:
        os.environ[serveritem.upper()] = ServerDictionary.get(serveritem)
        EnvServerKeys.append(serveritem.upper())
        # if print_env_params:
        #    print('......server env param: '+serveritem.upper()+' =', os.environ.get(serveritem.upper()))
    ######################################################################
    # move config params from ini file to os.envi as environment variables
    ######################################################################
    if server_ini_file and os.path.isfile(server_ini_file):
        if os.access(server_ini_file, os.R_OK):
            print('......server_ini_file FOUND...', server_ini_file)
            config = configparser.ConfigParser()
            config.read(server_ini_file)
            i = 0
            for section in config:
                i = i + 1
                k = 0
                if debug:
                    print('......', i, 'server.ini section =', section)
                for key in config[section]:
                    k = k + 1
                    os.environ[key.upper()] = config[section][key].replace("'", "")
                    EnvServerKeys.append(key.upper())
                    if debug:
                        print('.........', k, 'config_param', key.upper(), config[section][key])
                    # if print_env_params:
                    #    print('......server env param: '+key.upper()+' =', os.environ.get(key.upper()))
        else:
            print('......WARNING:', 'server_ini_file [', server_ini_file, '] is not readable')
    else:
        print('......WARNING:', 'server_ini_file NOT FOUND [', server_ini_file, ']')

    ######################################################################
    if str(os.environ.get('DEBUG_SERVER_STARTUP')).upper() in ('ON', '1', 'TRUE'):
        debug = True
        print_env_params = True
        print_all_env_params = True
    ######################################################################

    ######################################################################
    # save server.ini keys as env param
    ######################################################################
    strEnvServerKeys = str(EnvServerKeys)
    strEnvServerKeys = strEnvServerKeys.replace(']', '').replace('[', '').replace("'", "").replace(" ,", ",")
    strEnvServerKeys = strEnvServerKeys.replace(' ,', ',').replace(', ', ',')
    strEnvServerKeys = strEnvServerKeys.replace(' ,', '').replace(', ', '')
    strEnvServerKeys = strEnvServerKeys.replace(' ,', '').replace(', ', '')
    strEnvServerKeys = strEnvServerKeys.replace(' ,', '').replace(', ', '')
    #print("strEnvServerKeys =",strEnvServerKeys)
    os.environ['SERVER_INI_KEYS'] = strEnvServerKeys
    #print("EnvServerKeys =", os.environ.get('SERVER_INI_KEYS'))

    # ######################################################################
    # # move config params from ini file to os.envi as environment variables
    # ######################################################################
    # if server_config_file and os.path.isfile(server_config_file):
    #     if os.access(server_config_file, os.R_OK):
    #         print('......server_config_file FOUND...', server_config_file)
    #     else:
    #         print('......WARNING:', 'server_config_file [', server_config_file, '] is not readable')
    ######################################################################
    # list all env params
    ######################################################################
    if print_env_params:
        print('......Server Environment Variables:')
        for envitem in os.environ:
            if envitem in EnvServerKeys:
                print('...... server env param: '+envitem+' =', os.environ.get(envitem))

    if print_all_env_params:
        print('')
        print('......All Environment Variables:')
        for envitem in os.environ:
            if envitem not in EnvServerKeys:
                print('...... env param: '+envitem+' =', os.environ.get(envitem))
            else:
                print('...... ***server env param: '+envitem+' =', os.environ.get(envitem))

    print('...finish: server.ini')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    initialize_server(print_env_params='true')

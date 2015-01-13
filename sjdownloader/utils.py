'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Script for some utility functions.
It imports
    -os
    -time
    -json
It defines
    -opj
    -string_to_tuple
    -change_config
    -sanitize_string
    -file_size
    -write_downloads
    -write_history
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required Modules"""
import os
import time
import json

#------------------------------------------------------------------------------------------------------
def opj(path):
    '''
    Used for joining the current path into system path temporarily.
    '''
    root_path = os.path.dirname(__file__)
    cur_path = path.split('/')
    if cur_path[0] == '..':
        root_path = [root_path.replace(os.path.basename(root_path),'')]
        cur_path = cur_path[1:]
    else:
        root_path= [root_path]
    root_path.extend(cur_path)
    return apply(os.path.join,tuple(root_path))

#------------------------------------------------------------------------------------------------------
def dicts_to_tuples(dicts):
    '''
    converts a string of tuple into an actual tuple.
    Used for showing history.
    '''
    all_entries = []

    for dict in dicts:
        entry = (dict["URL"], dict["TIME"])
        all_entries.append(entry)

    return all_entries
#------------------------------------------------------------------------------------------------------
def change_config(dir_,filters,option,radio,segment):
    '''
    Function for writing configurations in config file.
    '''

    try:
        #--------------------First read the old date-------------------
        config_file = open(opj('config/config.json'),'r')
        data = json.load(config_file)
        config_file.close()

    except ValueError:
        #If file was empty
        data = {"configuration": {
                    "PATH": "", "FILTER": "", "OPTION": "",
                    "RENAME": "", "SEGMENT": ""}
                    }

    #-------------------Now write new data-------------------------
    config = data["configuration"]
    config["PATH"] = dir_
    config["FILTER"] = filters
    config["OPTION"] = option
    config["RENAME"] = radio
    config["SEGMENT"] = segment
    data = json.dumps(data)

    config_file = open(opj('config/config.json'),'w')
    config_file.write(data)
    config_file.close()
     
#------------------------------------------------------------------------------------------------------
def sanitize_string(string):
    '''
    function to trail whitespaces from strings
    '''
    if type(string) == list:
        for i,s in enumerate(string):
            string[i] = s.strip()
    else:
        strip = string.strip()

    return string

#------------------------------------------------------------------------------------------------------
def file_size(the_file):
    """
    Calculates the size of a file
    """
    with open(the_file) as my_file:
        data = my_file.read()
        size = len(data)

    return size

#------------------------------------------------------------------------------------------------------
def write_downloads(dl_list, clear=False):
    '''
    writing downloads in config file
    '''
    try:
        #------------------reading content file------------------------
        content_file = open(opj('config/content.json'))
        data = json.load(content_file)
        content_file.close()

    except ValueError:
        #If file was empty
        data = {"content": {
                    "DOWNLOADS": [],
                    "HISTORY": []
                    }
                }

    #-----------------------modifying content--------------------------
    #list of download entries
    downloads = data["content"]["DOWNLOADS"]

    if not clear:
        for dl in dl_list:
            downloads.append({"URL": dl, "TIME": time.ctime()})
    else:
        data["content"]["DOWNLOADS"] = []

    #----------------------writing content-----------------------------
    data = json.dumps(data)
    content_file = open(opj('config/content.json'),'w')
    content_file.write(data)
    content_file.close()

#------------------------------------------------------------------------------------------------------
def write_history(url, clear=False):
    '''
    writing history configurations to config file
    '''

    try:
        #------------------reading content file------------------------
        content_file = open(opj('config/content.json'))
        data = json.load(content_file)
        content_file.close()

    except ValueError:
        #If file was empty
        data = {"content": {
                    "DOWNLOADS": [
                        {"URL": "None", "TIME": "None"}
                        ],
                    "HISTORY": [
                        {"URL": "None", "TIME": "None"}
                        ]
                    }
                }

    #-----------------------modifying content--------------------------
    #list of download entries
    history = data["content"]["HISTORY"]

    if not clear:
        history.append({"URL": url, "TIME": time.ctime()})
    else:
        data["content"]["HISTORY"] = []

    #----------------------writing content-----------------------------
    data = json.dumps(data)
    content_file = open(opj('config/content.json'),'w')
    content_file.write(data)
    content_file.close()

#------------------------------------------------------------------------------------------------------


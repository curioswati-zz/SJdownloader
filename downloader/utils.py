'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Script for some utility functions.
It imports
    -os
It defines
    -opj
    -string_to_tuple
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required Modules"""
import os

#--------------------------------------------------------------------------
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

#--------------------------------------------------------------------------
def string_to_tuple(string):
    '''
    converts a string of tuple into an actual tuple.
    Used for showing history.
    >>>"[(url1,time1)\n(url2,time2)]"
    '''
    all_entries = []
    start = 1
    while True:
        end_entry = string.find('\n',start+1)
        if end_entry > 0:
            entry = string[start:end_entry]
            entry = tuple(entry.replace('(','').replace(')','').split(','))
            all_entries.append(entry)
            string = string[end_entry:]
        else:
            break
    return all_entries
#--------------------------------------------------------------------------
def change_config(dir_,filters,option,radio,history):
     dir_file = open(opj('config.txt'),'w')
     dir_file.write('PATH = '+dir_)
     dir_file.write("\n"+'FILTER = '+filters)
     dir_file.write("\n"+'OPTION = '+option)
     dir_file.write("\n"+'RENAME = '+radio)
     dir_file.write("\n"+'HISTORY = '+history)
     dir_file.close()

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

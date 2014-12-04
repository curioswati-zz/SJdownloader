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
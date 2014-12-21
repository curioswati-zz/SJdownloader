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
import time

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
#------------------------------------------------------------------------------------------------------
def change_config(dir_,filters,option,radio,history):
     dir_file = open(opj('config.txt'),'w')
     dir_file.write('PATH = '+dir_)
     dir_file.write("\n"+'FILTER = '+filters)
     dir_file.write("\n"+'OPTION = '+option)
     dir_file.write("\n"+'RENAME = '+radio+"\n")
     dir_file.close()
     
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

    DL_list = []
    for dl in dl_list:
        DL_list.append("("+time.ctime()+","+dl+")\n")

    #reading content file
    with open(opj('content.txt'),'r+') as content_file:
        data = content_file.read()
        download_point = data.find('DOWNLOADS')

        if download_point >= 0:
            if clear:
               DOWNLOADS = '[]' 
            else:
                end_point = data.find(']', download_point+1)
                DOWNLOADS = data[download_point+12:end_point+1]
            content_file.seek(download_point+1)        
        else:
            content_file.seek(-1,2)

        DOWNLOADS = DOWNLOADS[:-1] + ''.join(DL_list) + ']'
        #to avoid ioerror raised because of r+ mode
        content_file.truncate()
        content_file.write('DOWNLOADS = '+DOWNLOADS)

#------------------------------------------------------------------------------------------------------
def write_history(url, clear=False):
    '''
    writing history configurations to config file
    '''

    with open(opj('content.txt'),'r+') as content_file:
        data = content_file.read()
        content_file.seek(0)
        history_point = data.find('HISTORY')
        download_point = data.find("DOWNLOADS")

        if clear:
            if download_point > -1:
                #to avoid ioerror raised because of r+ mode
                content_file.truncate()
                content_file.write("HISTORY = []\n"+data[download_point:])
        else:
            if history_point >= 0:
                end_point = data.find(']', history_point+1)
                HISTORY = data[history_point+10:end_point+1]
            else:
                HISTORY = '[]'

            HISTORY = HISTORY[:-1] + "("+url+","+time.ctime()+")\n"+HISTORY[-1]
            print HISTORY

            #to avoid ioerror raised because of r+ mode
            content_file.truncate()
            content_file.write('HISTORY = '+HISTORY+"\n"+data[download_point:])

#------------------------------------------------------------------------------------------------------


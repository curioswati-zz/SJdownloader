import os
from join_path import opj
#------------------------------------------------------
    
def main(dir_,filters,option,history):
     print history
     dir_file = open(opj('config.txt'),'w')
     dir_file.write('PATH = '+dir_)
     dir_file.write("\n"+'FILTER = '+filters)
     dir_file.write("\n"+'OPTION = '+option)
     dir_file.write("\n"+'HISTORY = '+history)
     dir_file.close()

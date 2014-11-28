import os
from join_path import opj
#------------------------------------------------------
    
def main(dir_,filters):
     dir_file = open(opj('config.txt'),'w')
     dir_file.write(dir_)
     dir_file.write("\n"+filters)
     dir_file.close()

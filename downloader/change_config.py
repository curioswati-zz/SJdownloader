import os
def opj(path):
     return apply(os.path.join, tuple(path.split('/')))
#------------------------------------------------------
    
def main(dir_,filters):
     dir_file = open('/home/dc-19/Documents/GitHub/Downloader/downloader/config.txt','w')
     dir_file.write(dir_)
     dir_file.write("\n"+filters)
     dir_file.close()

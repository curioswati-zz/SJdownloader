import os

def opj(path):
    root_path = os.path.dirname(__file__)
    cur_path = path.split('/')
    if cur_path[0] == '..':
        root_path = [root_path.replace(os.path.basename(root_path),'')]
        cur_path = cur_path[1:]
    else:
        root_path= [root_path]
    root_path.extend(cur_path)
    return apply(os.path.join,tuple(root_path))
#------------------------------------------------------
##def opj(path):
##     #The path to join with root
##     cur_path = path.split('/')[1:]
##     #path from root to the dir, where script runs
##     root_path = os.path.dirname(__file__)
##     #removing the dir of script from above
##     root_path = root_path.replace(os.path.basename(root_path),'')
##     #join both paths
##     cur_path.insert(0,root_path)
##     print apply(os.path.join, tuple(cur_path))
##     return apply(os.path.join, tuple(cur_path))

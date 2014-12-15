'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''This script is used to download content from webpages
It Download the content from provided url.

It imports:
  -urllib
  
It defines:
  -Thread
    -__init__
    -run
  -Progress
    -__init__
    -updateProgress
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Required modules'''
import urllib
import wx
import time
import os
from threading import Thread
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from wx.lib.agw import pygauge as PG

from utils import opj
#---------------------------CONSTANTS---------------------------------------
#to check if file already exist
FILE_EXIST = None
#for reading rename option
rename = None
#the progress bar to be used in update_progress
progress = None

#Reading configuration file
def read_config():
    '''
    function to read config_file for rename option
    '''
    global rename

    with open(opj('config.txt')) as config_file:
        data = config_file.read()
        #rename option
    radio_point = data.find('RENAME')
    if radio_point > 0:
        end_point = data.find('\n',radio_point+1)
        rename = data[radio_point+9:end_point].strip()

#--------------------------------------------------------------------------
class TestThread(Thread):
    '''
    TestThread class to run the thread of downloading.
    '''
    def __init__(self,urls,path,stop):
        self.urls = urls
        self.path = path
        self.stop = stop
        Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    def run(self):
        time.sleep(1)
        global rename, FILE_EXIST

        read_config()
        dl_size = 0

        print "Downloading into "+self.path+"..."
        for url in self.urls:

            cancel = False
            
            f_name = os.path.basename(url)
            #Check if file exists and want to rename
            FILE_EXIST = os.path.exists(self.path+"/"+f_name)

            #IF default option is to cancel download, when already exist
            if FILE_EXIST and rename == 'Cancel':
                print f_name+" already exists, Canceling download"
                cancel = True
            
            #If default option is to rename new download, when already exist
            if FILE_EXIST and rename == 'Rename':
                count = 1
                old_f_name = f_name
                while True:
                    if os.path.exists(self.path+"/"+f_name):
                           tmp, ext = os.path.splitext(f_name)
                           cnt = "(%s)" % count
                           f_name = tmp+cnt+ext
                           count += 1
                           print f_name
                    else:
                        break
                print old_f_name+" already exist, renaming to "+f_name

            #If default option is to remove old download, when already exist                        
            elif FILE_EXIST and rename == 'Replace':
                os.remove(self.path+"/"+f_name)
                print f_name+" already exists, removing older one."

            if not cancel:
                try:
                    data = urllib.urlopen(url).read()
    #                req = requests.get(url,stream=True)
                    save_file = open(self.path+"/"+f_name, 'wb')
                    save_file.write(data)
                    dl_size += len(data)
                    save_file.close()
                    print f_name
                    wx.CallAfter(pub.sendMessage,"update",msg=dl_size)
#                    self.parent.Layout()
                except IOError:
                    return "The connection could not establish."
                except Exception as e:
                    return e

#--------------------------------------------------------------------------------------------------
def main(urls, path,progress_bar):
    '''
    Main module to call the TestThread for downloading and
    Progress to update the progress bar. It also calculates the size
    of file before downloading.
    '''    
    global progress
    progress = progress_bar

    #When called with direct url
    stop = False
    if (not(urls[0].startswith("http"))
        and ".html" not in urls[0]):
        return "Invalid url"
    #-----------------------------------------------------------------------------
    #Fetching file size before download
    try:
        total_size = 0
        for url in urls:
            connection = urllib.urlopen(url)
            meta = connection.info()
            try:
                size = float(meta.getheaders("content-length")[0])
                total_size += size
            except IndexError:
                size = len(connection.read())
                total_size += size
    except IOError:
        return "The connection could not establish"
    except Exception as e:
        return e

    #-----------------------------------------------------------------------------
    print_size = total_size/float(1024**2)
    print str(print_size) + "Mb selected for download"
    #-----------------------------------------------------------------------------

    #progress bar attributes
    progress_bar.SetBarColor([wx.Colour(162,255,178),wx.Colour(159,176,255)])
    progress_bar.SetBackgroundColour(wx.CYAN)
    progress_bar.SetBorderColor(wx.BLACK)
    progress_bar.SetBorderPadding(2)
    progress_bar.SetRange(total_size)

    #updating bar
    pub.subscribe(update_progress, "update")
    wx.Yield()
    #Start thread
    TestThread(urls, path,stop)

def update_progress(msg):
    '''
    updates the progress bar
    '''
    global progress
    progress.Update(msg,100)

#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main(url,dir_)

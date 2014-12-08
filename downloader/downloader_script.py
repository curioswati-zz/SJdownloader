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
#from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
from wx.lib.agw import pygauge as PG

from utils import opj
#---------------------------CONSTANTS---------------------------------------
#fetching configurations from config file
with open(opj('config.txt')) as config_file:
    data = config_file.read()
    #rename option
radio_point = data.find('RENAME')
end_point = data.find('\n',radio_point+1)
rename = data[radio_point+9:end_point]

#to check if file already exist
FILE_EXIST = None

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
        self.start()

    def run(self):
        global rename, FILE_EXIST
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
                    dl_size = len(data)
                    save_file.close()
                    print f_name
    #                wx.CallAfter(pub.sendMessage,"Update",msg=dl_size)
                except IOError as e:
                    return e
                    return "The connection could not establish."

#--------------------------------------------------------------------------------------------------
class Progress(wx.Gauge):
    '''
    Progress class to implement the updation of progress bar with
    an ongoing process of downloading.
    '''
    def __init__(self,progress,total_size):
        
        progress_bar = progress
        #progress bar attributes
        progress_bar.SetBarColor([wx.Colour(162,255,178),wx.Colour(159,176,255)])
        progress_bar.SetBackgroundColour(wx.CYAN)
        progress_bar.SetBorderColor(wx.BLACK)
        progress_bar.SetBorderPadding(2)
        progress_bar.SetRange(total_size)

        #updating bar
        pub.subscribe(self.updateProgress, "Update")

    #-----------------------------------------------------------------------------
    def updateProgress(self, msg):
        print "update:",msg
        progress_bar.Update(msg,100)

#--------------------------------------------------------------------------------------------------
def main(urls, path,progress_bar):
    '''
    Main module to call the TestThread for downloading and
    Progress to update the progress bar. It also calculates the size
    of file before downloading.
    '''    
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
    #-----------------------------------------------------------------------------
    #replaced by dl_size in `Thread`
    #update_value = total_size / len(urls)
    print_size = total_size/float(1024**2)
    print str(print_size) + "Mb selected for download"
    #-----------------------------------------------------------------------------
    #update the progress bar
    #Progress(progress_bar,total_size)
    #Start thread
    TestThread(urls, path,stop)
                
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main(url,dir_)



    
#-----------------------------------------------------------------------------------------------
#implement when requests downloaded
#writing byte by byte
##                for byte in req.iter_content(chunk_size=1024):
##                    if self.stop:
##                        break
##                    if byte:
##                        save_file.write(byte)
##                        save_file.flush()
##                    dl_size = len(byte)
##
##                    if dl_size < total_size:
##                        wx.CallAfter(pub.sendMessage,"update",msg=dl_size)
##
##    progress_bar.SetValue([0,total_size])   
##    progress_bar.SetDrawValue(draw=True, drawPercent=True, font=wx.SMALL_FONT, colour=wx.BLUE)

##            download_size = len(data)
#            percent = download_size / float(total_size)           

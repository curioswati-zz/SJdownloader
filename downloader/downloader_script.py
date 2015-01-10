'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''This script is used to download content from webpages
It Download the content from provided url.

It imports:
  -urllib2
  -wx
  -time
  -os
  -Thread from threading
  -setupkwargs from wx.lib.pubsub
  -pub from wx.lib.pubsub
  -pygauge from wx.lib.agw
  -opj from utils
  -utils
  
It defines:
  -read_config
  -Thread
    -__init__
    -run
  -main
  -update_progress
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Required modules'''
import urllib2
import wx
import time
import os
from threading import Thread
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from wx.lib.agw import pygauge as PG

from utils import opj
import utils
#---------------------------CONSTANTS---------------------------------------
#to check if file already exist
FILE_EXIST = None
#If partial file exist
PART_EXIST = None
#for reading rename option
RENAME = ''
#the progress bar to be used in update_progress
PROGRESS = None
#dictionary for files sizes
SIZE_DICT = {}
#To stop downloading
STOP = False
#segment option
SEGMENT = '1'

#--------------------------------------------------------------------------
#Reading configuration file
def read_config():
    '''
    function to read config_file for rename option
    '''
    global RENAME, SEGMENT

    with open(opj('config/config.txt')) as config_file:
        data = config_file.read()

    #rename option
    radio_point = data.find('RENAME')
    if radio_point >= 0:
        end_point = data.find('\n',radio_point+1)
        RENAME = data[radio_point+9:end_point].strip()

    #segment option
    segment_point = data.find('SEGMENT')
    if segment_point >= 0:
        end_point = data.find('\n',segment_point+1)
        SEGMENT = data[segment_point+10:end_point].strip()

    var = [RENAME, SEGMENT]

    #Trailing extra whitespaces
    RENAME, SEGMENT = utils.sanitize_string(var)

#---------------------------------------------------------------------------------------------------------------
class TestThread(Thread):
    '''
    TestThread class to run the thread of downloading.
    '''
    def __init__(self,urls,path):
        self.urls = urls
        self.path = path
        Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    #-----------------------------------------------------------------------------------------------------------
    def run(self):
        try:
            time.sleep(1)
            global RENAME, FILE_EXIST, PART_EXIST, PROGRESS, STOP, SEGMENT
            
            #--------------------------------reading configurations----------------------------------------
            read_config()
            print "Downloading into "+self.path+"..."

            for url in self.urls:

                dl_size = 0
                cancel = False

                f_name = os.path.basename(url)
                disk_file = self.path+"/"+f_name
                
                #Check if file exists and want to rename
                FILE_EXIST = os.path.exists(disk_file)
                
                #----------------IF default option is to cancel download, when already exist---------------
                if FILE_EXIST and RENAME == 'Cancel':
                    dlg = wx.MessageDialog(PROGRESS.Parent,f_name+" already exists, Canceling download",
                                           'Oops!', wx.OK|wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()

                    cancel = True

                #---------------If default option is to rename new download, when already exist------------
                if FILE_EXIST and RENAME == 'Rename':
                    count = 1
                    old_f_name = f_name
                    while True:
                        if os.path.exists(disk_file):
                               tmp, ext = os.path.splitext(f_name)
                               cnt = "(%s)" % count
                               if count > 1:
                                tmp = tmp[:-3]
                               f_name = tmp+cnt+ext
                               count += 1
                               print f_name
                               disk_file = self.path+"/"+f_name
                        else:
                            break
                    dlg = wx.MessageDialog(PROGRESS.Parent,old_f_name+" already exist, renaming to "+f_name,
                                           'Oops!', wx.OK|wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()

                #----------------If default option is to remove old download, when already exist-----------
                elif FILE_EXIST and RENAME == 'Replace':
                    os.remove(disk_file)
                    dlg = wx.MessageDialog(PROGRESS.Parent,f_name+" already exists, removing older one.",
                                           'Oops!', wx.OK|wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    dlg.Destroy()

                PART_EXIST = os.path.exists(disk_file+"_part")

                #-----------------------Begin Process-------------------------------------------------------
                if not cancel:

                    seek_point = 0

                    #----------------If a partial file exists, remove `_part` string------------------------
                    if PART_EXIST:
                        size_of_file = utils.file_size(disk_file+"_part")
                        if size_of_file < SIZE_DICT[url]:
                            seek_point = size_of_file+1
                            print 'seek_point: ',seek_point

                    #--------------------Downloading the file-----------------------------------------------
                    try:
                        #------------------Setup connection-------------------------------------------------
                        req = urllib2.Request(url)
                        req.headers["Range"]="bytes=%s-%s" % (seek_point, int(SIZE_DICT[url]))
                        connection = urllib2.urlopen(req)

                        #------------------If server does not accept range-header---------------------------
                        status_code = connection.getcode()
                        if  status_code== 200 and PART_EXIST:
                            dlg = wx.MessageDialog(PROGRESS.Parent,"Partial content not allowed, starting download from beginning",
                                           'Oops!', wx.OK|wx.ICON_INFORMATION)
                            dlg.ShowModal()
                            dlg.Destroy()
                            print "Partial content not allowed, starting download from beginning"

                        print connection.getcode()

                        #--------------------open disk file for writing-------------------------------------
                        if PART_EXIST and not (status_code == 200):
                            save_file = open(disk_file+"_part", 'ab+')
                        else:
                            save_file = open(disk_file, 'wb')                          

                        if SEGMENT == '1' or SEGMENT == "Default":
                            block_sz = 1024
                        else:
                            block_sz = int(SIZE_DICT[url] / int(SEGMENT))

                        print block_sz

                        #-------------------------Setting the progress bar ---------------------------------
                        PROGRESS.SetRange(SIZE_DICT[url] - seek_point)
                        PROGRESS.SetValue(0)
                        PROGRESS.Parent.Refresh()

                        #--------------------------Saving Content-------------------------------------------
                        while True:
                            buffer = connection.read(block_sz)
                            if not buffer:
                                break
                            if STOP:
                                STOP = False
                                raise IOError
                            dl_size += len(buffer)
                            save_file.write(buffer)
                            save_file.flush()
                            wx.CallAfter(pub.sendMessage,"update",msg=dl_size)

                        #-------------------------Close the file--------------------------------------------
                        save_file.close()
                        print f_name+" downloaded"

                        #----------------------If it was a part file, rename it to original-----------------
                        if PART_EXIST:
                            old_name = disk_file+"_part"

                            #need to reformat the name to avooid the rename error:
                                # The name of file is incorrect in windows
                            new_name = old_name.split("/")[0]+"\\"+old_name.split("/")[1][:-5]

                            os.rename(old_name,new_name)

                    except IOError:
                        #--------------If file was not downloaded completely, mark it as part---------------
                        if dl_size < SIZE_DICT[url]:
                            try:
                                save_file.close()
                            except:
                                pass
                            if not PART_EXIST:
                                os.rename(disk_file,disk_file+"_part")
                            print disk_file

                        dlg = wx.MessageDialog(PROGRESS.Parent,"The connection was broken.",
                                           'Oops!', wx.OK|wx.ICON_INFORMATION)
                        dlg.ShowModal()
                        dlg.Destroy()

                    except Exception as e:
                        print e
                        dlg = wx.MessageDialog(PROGRESS.Parent,str(e),
                                           'Oops!', wx.OK|wx.ICON_INFORMATION)
                        dlg.ShowModal()
                        dlg.Destroy()

        except Exception as e:
            print 'Exception:',e

#---------------------------------------------------------------------------------------------------------------
def main(urls, path,progress_bar):
    '''
    Main module to call the TestThread for downloading and
    to set attributes of the progress bar. It also calculates the size
    of file before downloading.
    '''    
    global PROGRESS, SIZE_DICT
    PROGRESS = progress_bar

    #When called with direct url
    if (not(urls[0].startswith("http"))
        and ".html" not in urls[0]):
        return "Invalid url"
    #-------------------Fetching file size before download------------------------
    try:
        total_size = 0
        for url in urls:
            connection = urllib2.urlopen(url)
            meta = connection.info()
            try:
                size = float(meta.getheaders("content-length")[0])
                total_size += size
                SIZE_DICT[url] = size
            except IndexError:
                size = len(connection.read())
                total_size += size
                SIZE_DICT[url] = size
    except IOError:
        return "The connection could not establish"
    except Exception as e:
        return e

    #-----------------------------------------------------------------------------
    print_size = total_size/float(1024**2)
    print str(print_size) + "Mb selected for download"
    #-----------------------------------------------------------------------------

    #------------------------progress bar attributes------------------------------
    progress_bar.SetBarColor([wx.Colour(162,255,178),wx.Colour(159,176,255)])
    progress_bar.SetBackgroundColour(wx.CYAN)
    progress_bar.SetBorderColor(wx.BLACK)
    progress_bar.SetBorderPadding(2)
    print 'total_size:',total_size

    #updating bar
    pub.subscribe(update_progress, "update")
    wx.Yield()
    #--------------------------Start thread---------------------------------------
    TestThread(urls, path)

#---------------------------------------------------------------------------------------------------------------
def update_progress(msg):
    '''
    updates the progress bar.
    '''
    global PROGRESS
    print 'msg:',msg
    PROGRESS.SetValue(msg)
    PROGRESS.Parent.Refresh()

#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main(url,dir_)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This is the Mypanel class for GUI module.
It creates the widgets like buttons and textAreas; packs them into container.
It also implements the binding of buttons to various events using functions to
filter, browse location, and download content.

It imports:
    -wx
    -re
    -get_urls
    -downloader_script
It defines:
    -__init__
    -EvtCheckBox
    -enter
    -download
    -browse
    -reset
    -filter
    -EvtCheckListBox
    -close
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required modules"""
import re,os
import wx
from wx.lib.agw import aquabutton as AB
from wx.lib.agw import pygauge as PG

import get_urls,downloader_script
from class_FlatMenu import Menu
from class_preferences import open_pref

#modifying path for logo
def opj(path):
     return apply(os.path.join, tuple(path.split('/')))
#------------------------------------------------------

class Mypanel(object):
    def __init__(self,panel,win):
        self.win = win                                                      #The window object
        self.panel = panel                                                  #The panel object

        box = wx.StaticBox(self.panel, -1,size=(2000,80))
        self.introsizer = wx.StaticBoxSizer(box)

        #LOGO
        png = wx.Image(opj('../Icons/Logo.png'),
                       wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        logo = wx.StaticBitmap(panel, -1, png,(10,30))

        #Description
        sub_container = wx.BoxSizer(wx.VERTICAL)
        description = wx.TextCtrl(self.panel, -1,size=(580,50))
        description.SetEditable(False)
        description.SetValue("A free internet downloader, Now download It all,just enter the url and click start!")
        
        description.SetBackgroundColour((198,222,223,255))
        sub_container.Add(description,proportion=0)
        
        self.introsizer.Add(logo,proportion=0)
        self.introsizer.Add(sub_container,proportion=1,flag=wx.EXPAND)
        #--------------------------------------------------------------------------
        #creating buttons, and binding events with them, that occurs on click.

        #calls (enter) method
        show_btn = AB.AquaButton(panel, -1, None, "Show Links",size=(80,30))
        show_btn.SetBackgroundColour((198,222,223,255))
        show_btn.SetForegroundColour("Black")
        show_btn.SetToolTipString("Click to show found links")
        show_btn.Bind(wx.EVT_BUTTON,self.enter)

        #calls browse method;
        browse_btn = wx.BitmapButton(self.panel, -1,
                                     wx.Bitmap('../Icons/folder.png'))
        browse_btn.SetBackgroundColour((198,222,223,255))
        browse_btn.SetForegroundColour("Black")
        browse_btn.SetToolTipString("Select location")
        browse_btn.Bind(wx.EVT_BUTTON,self.browse)
        
        #calls reset method
        reset_btn = AB.AquaButton(panel, -1, None, "Reset",size=(80,30))
        reset_btn.SetBackgroundColour((198,222,223,255))
        reset_btn.SetForegroundColour("Black")
        reset_btn.SetToolTipString("Reset downloader")
        reset_btn.Bind(wx.EVT_BUTTON,self.reset)

        #calls download metod
        self.download_btn = AB.AquaButton(panel, -1, None, "Start",size=(80,30))
        self.download_btn.SetBackgroundColour((198,222,223,255))
        self.download_btn.SetForegroundColour("Black")
        self.download_btn.SetToolTipString("Start download")
        self.download_btn.Bind(wx.EVT_BUTTON,self.download)
        
        close_btn = AB.AquaButton(panel, -1, None, "Close",size=(80,30))
        close_btn.SetBackgroundColour((198,222,223,255))
        close_btn.SetForegroundColour("Black")
        close_btn.SetToolTipString("Close")
        close_btn.Bind(wx.EVT_BUTTON,self.close)
        
        cancel_btn = AB.AquaButton(panel, -1, None, "Cancel",size=(80,30))
        cancel_btn.SetBackgroundColour((198,222,223,255))
        cancel_btn.SetForegroundColour("Black")
        cancel_btn.SetToolTipString("Cancel download")
        cancel_btn.Bind(wx.EVT_BUTTON,self.cancel)

        #calls filter method
        self.filter_btn = AB.AquaButton(panel, -1, None, "Filter",size=(60,30))
        self.filter_btn.SetBackgroundColour((198,222,223,255))
        self.filter_btn.SetForegroundColour("Black")
        self.filter_btn.SetToolTipString("Filter links")
        self.filter_btn.Bind(wx.EVT_BUTTON,self.filter)
        self.filter_btn.Disable()
        
        #--------------------------------------------------------------------------
        #defining text areas; to input text
        '''
        >>>"http://www.google.com/" -> keyed in url_field
        calls (enter)
        >>>C:\Python27 -> keyed in dir
        >>>.*.jpg -> keyed in regex
        '''

        #Static text area:

        #Label, before text box for url
        url = wx.StaticText(panel, -1, "URL:",size=(70,25))   
        #Label, before text box for dir location
        location = wx.StaticText(panel, -1, "Save file in:",size=(80,25))
        #Count of links
        self.count = wx.StaticText(self.panel,-1,"No. of links found:",
                                       size=(255,15),pos=(420,295))
        #Label, before regex text box
        regex = wx.StaticText(panel, -1, "Enter regex:",pos=(400,310))
        #progress label
        progress = wx.StaticText(panel, -1, "Progress")

        #--------------------------------------------------------------------------
 
        #text box for url, calls (enter) method on text event
        self.url_field = wx.TextCtrl(panel,
                                     size=(400,20),pos=(5,5),                                     
                                     style=wx.TE_PROCESS_ENTER,
                                     )
        self.url_field.SetToolTipString("Enter url here");
        #self.url_field.Bind(wx.EVT_TEXT, self.enter)                                                                   
        
        #text box for showing dir location
        self.dir = wx.TextCtrl(panel,size=(400,25),pos=(5,30))
        self.dir.SetToolTipString("Selected location to save file");

        #Static box For showing links
        self.box = wx.StaticBox(self.panel, -1, "The links will be shown here")
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)

        #text box for entering regex pattern
        self.regex = wx.TextCtrl(panel,size=(255,25))
        self.regex.SetToolTipString("Enter type string to filter content");
        self.regex.SetEditable(False)
        #Progress bar
        self.progress = PG.PyGauge(panel,-1,size=(330,25),style=wx.GA_HORIZONTAL)

        #--------------------------------------------------------------------------
        #Defining CheckBoxes

        self.cb1 = wx.CheckBox(panel, -1, "jpeg",
                          (5, 295), (75, 20))
        self.cb2 = wx.CheckBox(panel, -1, "png",
                          (5, 310), (75, 20))
        self.cb3 = wx.CheckBox(panel, -1, "gif",
                          (5, 335), (75, 20))
        self.cb4 = wx.CheckBox(panel, -1, "mp4",
                          (35, 295), (75, 20))
        self.cb5 = wx.CheckBox(panel, -1, "3gp",
                          (35,310), (75, 20))
        self.cb6 = wx.CheckBox(panel, -1, "avi",
                          (35, 335), (75, 20))
        self.cb7 = wx.CheckBox(panel, -1, "flv",
                          (70, 295), (55, 20))
        self.cb8 = wx.CheckBox(panel, -1, "mp3",
                          (70, 310), (55, 20))
        self.cb9 = wx.CheckBox(panel, -1, "jpg",
                          (70, 310), (55, 20))
        selectAll = wx.CheckBox(self.panel, -1, "select all",
                              (70, 310), (85, 15))
        
        #Binding events with checkboxes
        
        self.cb1.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb1.Enable(False)
        self.cb2.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb2.Enable(False)
        self.cb3.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb3.Enable(False)
        self.cb4.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb4.Enable(False)
        self.cb5.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb5.Enable(False)
        self.cb6.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb6.Enable(False)
        self.cb7.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb7.Enable(False)
        self.cb8.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb8.Enable(False)
        self.cb9.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        self.cb9.Enable(False)
        selectAll.Bind(wx.EVT_CHECKBOX, self.select_all)

        #--------------------------------------------------------------------------

        #WRAPPING UP THE BOXES
        #----------------------
        #The text controls
        #-----------------

        #The url, url label containers                           Container#1
        url_box = wx.BoxSizer()                                  
        url_box.Add(url,proportion=0,flag=wx.TOP|wx.RIGHT,border=7)
        url_box.Add(self.url_field,proportion=1,flag=wx.EXPAND|
                    wx.ALL,border=5)
        url_box.Add(show_btn,proportion=0,border=5,flag=wx.ALL)

        #The dir location, location label container              Container#2 
        dir_box = wx.BoxSizer()
        dir_box.Add(location,proportion=0,flag=wx.TOP|wx.RIGHT,border=5)
        dir_box.Add(self.dir,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        dir_box.Add(browse_btn,proportion=0,border=5,flag=wx.ALL)
        #--------------------------------------------------------------------------
        #For select all and count box
        self.hbox = wx.FlexGridSizer(cols=2, vgap=10, hgap=350)
        self.hbox.Add(selectAll,proportion=0,flag=wx.TOP|wx.LEFT|
                      wx.RIGHT,border=5)
        self.hbox.Add(self.count,proportion=1,flag=wx.TOP|wx.LEFT|
                      wx.RIGHT,border=5)
        
        #container for main output box                           Container#3
        Static_box = wx.BoxSizer()
        Static_box.Add(self.bsizer,proportion=1,flag=wx.EXPAND
                  |wx.ALL,border=5
                  )
        Static_box.Add(reset_btn,proportion=0,border=5,flag=wx.ALL)
        #--------------------------------------------------------------------------

        #--------------
        #The checkBoxes
        #--------------
        #First set of boxes vertically
        feature_box1 = wx.BoxSizer(wx.VERTICAL)
        
        feature_box1.Add(self.cb1, proportion=0,flag=wx.EXPAND     #jpeg
                      |wx.LEFT|wx.BOTTOM,border=5)
        feature_box1.Add(self.cb2, proportion=0,flag=wx.EXPAND     #png
                      |wx.LEFT|wx.BOTTOM,border=5)
        feature_box1.Add(self.cb3, proportion=0,flag=wx.EXPAND     #gif
                      |wx.LEFT|wx.BOTTOM,border=5)

        #Second set of boxes vertically
        feature_box2 = wx.BoxSizer(wx.VERTICAL)
        feature_box2.Add(self.cb4, proportion=0,flag=wx.EXPAND     #mp4
                      |wx.ALL,border=2)
        feature_box2.Add(self.cb5, proportion=0,flag=wx.EXPAND     #3gp
                      |wx.ALL,border=2)
        feature_box2.Add(self.cb6, proportion=0,flag=wx.EXPAND     #avi
                      |wx.ALL,border=2)

        #Third set of boxes vertically
        feature_box3 = wx.BoxSizer(wx.VERTICAL)
        feature_box3.Add(self.cb7, proportion=0,flag=wx.EXPAND     #flv
                      |wx.ALL,border=2)
        feature_box3.Add(self.cb8, proportion=0,flag=wx.EXPAND     #mp3
                      |wx.ALL,border=2)
        feature_box3.Add(self.cb9, proportion=0,flag=wx.EXPAND     #jpg
                      |wx.ALL,border=2)
        #--------------------------------------------------------------------------
        
        #-------------------
        #Extra feature boxes
        #-------------------
        #container for regex text box and filter button
        regex_box = wx.FlexGridSizer(cols=3, vgap=10, hgap=3)
        regex_box.Add(regex,proportion=0,flag=wx.TOP,border=7)
        regex_box.Add(self.regex,proportion=1,flag=wx.BOTTOM|wx.LEFT|wx.EXPAND,border=5)
        regex_box.Add(self.filter_btn,proportion=0,flag=wx.ALL,border=5)

        #container for (regex,filter) container and count text box
        feature_box4 = wx.BoxSizer(wx.VERTICAL)
        #feature_box4.Add(self.count,proportion=1,flag=wx.TOP,border=5)
        feature_box4.Add(regex_box,proportion=1,flag=wx.ALL)

        #--------------------------------------------------------------------------
        #container for (checkbox, extra feature) containers     Container#4
        feature_box = wx.BoxSizer()
        feature_box.Add(feature_box1,proportion=0)
        feature_box.Add(feature_box2,proportion=0)
        feature_box.Add(feature_box3,proportion=0)
        feature_box.Add(feature_box4,proportion=0,flag=wx.EXPAND)

        #--------------------------------------------------------------------------

        #container for progres bar                              Container#5
        prog_box = wx.BoxSizer()
        prog_box.Add(progress, proportion=0, flag=wx.ALL,border=10)
        prog_box.Add(self.progress,proportion=1,
                     flag=wx.ALL,border=10)
        prog_box.Add(self.download_btn,proportion=0,border=5,
                     flag=wx.RIGHT|wx.TOP|wx.BOTTOM)
        prog_box.Add(cancel_btn, proportion=0, border=5,
                      flag=wx.ALL)
        prog_box.Add(close_btn, proportion=0,border=5,
                     flag=wx.LEFT|wx.TOP)

        #--------------------------------------------------------------------------      
        #container for introsizer and Containers #1,#2,#3,#4,#5
        #-------------------------------------------
        self.main_container = wx.BoxSizer(wx.VERTICAL)
        sub_container.Add(url_box,proportion=1)
        sub_container.Add(dir_box,proportion=1)
        self.main_container.Add(self.introsizer,proportion = 0)
        self.main_container.Add(self.hbox,proportion=0,flag=wx.EXPAND)
        self.main_container.Hide(self.hbox)
        self.panel.Layout()
        self.main_container.Add(Static_box,proportion=1,
                           flag=wx.EXPAND)
        self.main_container.Add(feature_box,proportion=0)
        self.main_container.Add(prog_box,proportion=0)
      
        panel.SetSizer(self.main_container)
        #--------------------------------------------------------------------------
        
        #an empty list for showing filtered links.
        self.filtered = []
        #for keeping track of old regex filtered list; used in (filter)
        self.old_filtered = []
        #List for checked links to download;
         #used in (enter),(filter),(EvtCheckBox)
        self.toDownload = []
        menu = Menu(self.win)
        
    #--------------------------------------------------------------------------
    def EvtCheckBox(self, event):
        check_box = event.GetEventObject()
        regex = '.*\.'+check_box.GetLabelText()                       #creating a regex pattern based on
                                                                      #the label str of selected checkbox.
        try:            
            pattern = re.compile(regex)
            filtered = re.findall(regex, '\n'.join(self.urls))

            if event.IsChecked():
                self.filtered.extend(filtered)

            if not event.IsChecked():
                for item in filtered:
                    self.filtered.remove(item)

            if filtered:

                if self.filtered:
                    self.box.SetLabel("")
                    self.check_list.SetItems(self.filtered)
                    self.main_container.Show(self.hbox)
                    self.panel.Layout()
                    self.count.SetLabel("No. of links found: "+str(len(self.filtered)))
                    
                elif not(event.IsChecked()):
                    self.box.SetLabel("")
                    self.check_list.SetItems(self.urls)
                    self.main_container.Show(self.hbox)
                    self.panel.Layout()
                    self.count.SetLabel("No. of links found: "+str(len(self.urls)))
                    
            elif not(event.IsChecked()):
                self.box.SetLabel("")
                self.check_list.SetItems(self.urls)
                self.main_container.Show(self.hbox)
                self.panel.Layout()                    
                self.count.SetLabel("No. of links found: "+str(len(self.urls)))

            else:
                self.check_list.SetItems(self.filtered)
                self.box.SetLabel("No links matched, try another filter; or to show all links, click 'show links' button")
                self.main_container.Hide(self.hbox)
                self.panel.Layout()

            self.toDownload = []            
            self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox) 
            self.check_list.SetSelection(0)
        except:
            pass
            
    #--------------------------------------------------------------------------
    def select_all(self, event):
        if event.IsChecked():
            if self.filtered:
                 try:
                    self.toDownload = self.filtered
                    indices = range(len(self.toDownload))
                    self.check_list.SetChecked(indices)
                 except Exception as e:
                     print e
            else:
                try:
                    self.toDownload = self.urls
                    indices = range(len(self.toDownload))
                    self.check_list.SetChecked(indices)
                except Exception as e:
                    print e
        else:
            try:
                for index in xrange(len(self.toDownload)):
                    self.check_list.Check(index,False)
            except:
                pass

    #--------------------------------------------------------------------------
    def enter(self, event):
        '''
        The function to prepare a list of all urls found on home page,
        It works on text_enter_event of textctrl box called 'url'.
        '''
        
        #Fetching urls
        home_url = self.url_field.GetValue().strip()
        if home_url == "":
            self.url_field.SetValue("Please enter url")
            return
        error, self.urls = get_urls.main(home_url)

        #if urls fetched
        if self.urls:
            
            self.main_container.Show(self.hbox)
            #Enabling the checkboxes, and buttons
            self.cb1.Enable(True)
            self.cb2.Enable(True)
            self.cb3.Enable(True)
            self.cb4.Enable(True)
            self.cb5.Enable(True)
            self.cb6.Enable(True)
            self.cb7.Enable(True)
            self.cb8.Enable(True)
            self.cb9.Enable(True)

            self.filter_btn.Enable()
            self.regex.SetEditable(True)

            #--------------------------------------------------------------
            #Creating check list box
            try:
                self.check_list.Destroy()
                self.filtered = []
            except:
                pass

            self.check_list = wx.CheckListBox(self.panel, -1, (5,180),
                                              (583,240),self.urls,
                                              style = wx.HSCROLL)
            self.count.SetLabel("No. of links found: "+str(len(self.urls)))
            self.box.SetLabel("")
            
            self.bsizer.Add(self.check_list,proportion=1,flag=wx.EXPAND
                      |wx.ALL,border=5
                      )
                      
            self.panel.Layout()

            self.toDownload = []
            self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox)
        else:
            print error
            
    #--------------------------------------------------------------------------
    def filter(self,event):
        '''
        The function filters links found on the page.
        It uses regex to filter and display a list of urls matching the pattern.
        The pattern is specified in the box called regex.
        '''

        pattern = self.regex.GetValue()
        try:
             if self.urls:
                 filtered = None
                 if pattern:
                     pattern = re.compile(pattern)
                     filtered = re.findall(pattern,'\n'.join(self.urls))
                     self.filtered.extend(filtered)
                     self.old_filtered = filtered

                 else:
                     for item in self.old_filtered:
                         self.filtered.remove(item)
                         
                 if not filtered:
                     self.box.SetLabel("No links matched, try another filter; or to show all links, click 'show links' button")

                 if self.filtered:
                     self.check_list.SetItems(self.filtered)
                     self.count.SetLabel("No. of links found: "+str(len(self.filtered)))
                 else:
                     self.box.SetLabel("No links matched, try another filter; or to show all links, click 'show links' button")
                     self.check_list.SetItems("")
                     self.main_container.Hide(self.hbox)
                     self.panel.Layout()

                 #list of selected links
                 self.toDownload = []
                 
                 self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox) 
                 self.check_list.SetSelection(0)
        except Exception as e:
            print e
        
    def EvtCheckListBox(self, event):
        '''
        Function to implement checking and unchecking of list items.
        Also, according to checking and unchecking, adds and removes
        items to/from download list.
        '''
        index = event.GetSelection()
        label = self.check_list.GetString(index)
        status = 'un'
        string_at_index = self.check_list.GetString(index)
        
        if self.check_list.IsChecked(index):
            status = ''
            self.check_list.SetSelection(index)                             #so that (un)checking also selects (moves the highlight)
        #print self.toDownload

    #--------------------------------------------------------------------------
    def download(self,event):
        '''
        The function is bind with download button and download the content.
        It fetches urls from the 'contents' textctrl and sends urls to
        downloader_script.
        Uses 'browse' filedialogs current path to save files.
        '''

        if not(self.url_field.GetValue() == ""):                           #If url field is not empty
            if self.dir.GetValue() == "":                                  #if dir field is empty
                
                #file_default_dir = open('default_dir.txt','r')
                #default_dir = str(file_default_dir.read())
                #file_default_dir.close()

                #print default_dir
                self.dir.SetValue('.')
                self.path = '.'
            try:
                self.toDownload.extend(self.check_list.GetCheckedStrings())
                urls_to_download = self.toDownload
                
                error = downloader_script.main(urls_to_download,self.path,
                                               self.progress)
    
            except AttributeError:
                error = downloader_script.main([self.url_field.GetValue().strip()],self.path,
                                               self.progress)
            if error:
                print error
                dlg = wx.MessageDialog(self.panel,"Connection failed",
                                       'Oops!', wx.OK|wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            
        else:
            self.url_field.SetValue("Please Enter url")

    #--------------------------------------------------------------------------
    def browse(self,event):
        '''
        The function is bind with the browse button.
        It opens a directory location.
        Treats the dir input in dir_ box as the default.
        '''
        
        dir_= self.dir.GetValue()
        dlg = wx.DirDialog(self.win, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           | wx.DD_CHANGE_DIR
                           )

        dlg.SetPath(dir_)
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
            self.dir.SetValue(self.path)

        dlg.Destroy()
        
    #--------------------------------------------------------------------------
    def reset(self,event):
        '''
        This is bound to reset button, when pressed, it clears all text areas.
        '''
        self.url_field.SetValue(" ")
        try:
            self.check_list.Destroy()
        except Exception:
            pass
        self.regex.SetValue(" ")
        self.dir.SetValue(" ")
        self.path = " "
        self.box.SetLabel("The links will be shown here")
        self.main_container.Hide(self.hbox)
        
        #Disabling all checkboxes
        self.cb1.Enable(False)
        self.cb2.Enable(False)
        self.cb3.Enable(False)
        self.cb4.Enable(False)
        self.cb5.Enable(False)
        self.cb6.Enable(False)
        self.cb7.Enable(False)
        self.cb8.Enable(False)
        self.cb8.Enable(False)
        
        self.filter_btn.Disable()        
        self.regex.SetEditable(False)
        
        self.panel.Layout()

    #--------------------------------------------------------------------------
    def cancel(self, event):
        downloader_script.stop = True
        self.win.Destroy()
    
    def close(self, event):
        self.win.Destroy()

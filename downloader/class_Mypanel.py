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
import wx
import get_urls,downloader_script
import re,os

class Mypanel(object):
    def __init__(self,panel,win):
        self.win = win                                                      #The window object
        self.panel = panel                                                  #The panel object

        box = wx.StaticBox(self.panel, -1, "The intro Box",size=(800,400))
        self.introsizer = wx.StaticBoxSizer(box)
        #--------------------------------------------------------------------------
        #creating buttons, and binding events with them, that occurs on click.

        #calls (enter) method
        show_btn = wx.Button(panel,label = "Show Links",size=(80,25))
        show_btn.Bind(wx.EVT_BUTTON,self.enter)
        show_btn.SetToolTipString("Click to show found links")

        #calls browse method;
        browse_btn = wx.Button(panel,label = "browse",size=(80,25))
        browse_btn.Bind(wx.EVT_BUTTON,self.browse)
        browse_btn.SetToolTipString("Select location")

        #calls reset method
        reset_btn = wx.Button(panel,label = "Reset",size=(80,25))
        reset_btn.Bind(wx.EVT_BUTTON,self.reset)
        reset_btn.SetToolTipString("Reset downloader")

        #calls download metod
        download_btn = wx.Button(panel,label = "download",size=(80,25))
        download_btn.Bind(wx.EVT_BUTTON,self.download)
        download_btn.SetToolTipString("Start download")

        #calls filter method
        filter_btn = wx.Button(panel,label="Filter",size=(60,25),style=wx.NO_BORDER)
        filter_btn.Bind(wx.EVT_BUTTON,self.filter)
        filter_btn.SetToolTipString("Filter links")

        #--------------------------------------------------------------------------
        #defining text areas; to input text
        '''
        >>>"http://www.google.com/" -> keyed in url_field
        calls (enter)
        >>>C:\Python27 -> keyed in dir
        >>>.*.jpg -> keyed in regex
        '''
        
        #Static text label, before text box for url
        url = wx.StaticText(panel, -1, "URL:",size=(60,25))
        #text box for url, calls (enter) method on text event
        self.url_field = wx.TextCtrl(panel,
                                     size=(415,25),pos=(5,5),                                     
                                     style=wx.TE_PROCESS_ENTER,
                                     )
        self.url_field.SetToolTipString("Enter url here");
        self.url_field.Bind(wx.EVT_TEXT, self.enter)                                                                   
        
        #Static text label, before text box for dir location
        location = wx.StaticText(panel, -1, "Save file in:")
        #text box for showing dir location
        self.dir = wx.TextCtrl(panel,size=(415,25),pos=(5,30))
        self.dir.SetToolTipString("Selected location to save file");

        #Static box For showing links
        box = wx.StaticBox(self.panel, -1, "The links will be shown here")
        self.bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        #Static box for showing count of links        
        self.count = wx.StaticText(panel,-1,"No. of links found:",size=(255,15),pos=(420,295))
        #Static text label, before regex text box
        regex = wx.StaticText(panel, -1, "Enter regex:",pos=(400,310))
        #text box for entering regex pattern
        self.regex = wx.TextCtrl(panel,size=(255,25))
        self.regex.SetToolTipString("Enter type string to filter content");
        #Progress bar
        self.progress = wx.TextCtrl(panel,size=(390,25),pos=(5,335))

        #--------------------------------------------------------------------------
        #Defining CheckBoxes

        cb1 = wx.CheckBox(panel, -1, "jpeg",
                          (5, 295), (75, 25))
        cb2 = wx.CheckBox(panel, -1, "png",
                          (5, 310), (75, 25))
        cb3 = wx.CheckBox(panel, -1, "gif",
                          (5, 335), (75, 25))
        cb4 = wx.CheckBox(panel, -1, "mp4",
                          (35, 295), (75, 25))
        cb5 = wx.CheckBox(panel, -1, "3gp",
                          (35,310), (75, 25))
        cb6 = wx.CheckBox(panel, -1, "avi",
                          (35, 335), (75, 25))
        cb7 = wx.CheckBox(panel, -1, "flv",
                          (70, 295), (55, 25))
        cb8 = wx.CheckBox(panel, -1, "mp3",
                          (70, 310), (55, 25))

        #Binding events with checkboxes
        
        cb1.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        cb2.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        cb3.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        cb4.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        cb5.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        cb6.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        cb7.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)
        cb8.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox)

        #--------------------------------------------------------------------------

        #WRAPPING UP THE BOXES
        #----------------------
        #The text controls
        #-----------------

        #The url, url label containers                           Container#1
        url_box = wx.BoxSizer()                                  
        url_box.Add(url,proportion=0,flag=wx.TOP|wx.LEFT,border=10)
        url_box.Add(self.url_field,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        url_box.Add(show_btn,proportion=0,border=5,flag=wx.ALL)

        #The dir location, location label container              Container#2 
        dir_box = wx.BoxSizer()
        dir_box.Add(location,proportion=0,flag=wx.ALL,border=5)
        dir_box.Add(self.dir,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        dir_box.Add(browse_btn,proportion=0,border=5,flag=wx.ALL)
        #--------------------------------------------------------------------------

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
        
        feature_box1.Add(cb1, proportion=0,flag=wx.EXPAND     #jpeg
                      |wx.LEFT|wx.BOTTOM,border=5)
        feature_box1.Add(cb2, proportion=0,flag=wx.EXPAND     #png
                      |wx.LEFT|wx.BOTTOM,border=5)
        feature_box1.Add(cb3, proportion=0,flag=wx.EXPAND     #gif
                      |wx.LEFT|wx.BOTTOM,border=5)

        #Second set of boxes vertically
        feature_box2 = wx.BoxSizer(wx.VERTICAL)
        feature_box2.Add(cb4, proportion=0,flag=wx.EXPAND     #mp4
                      |wx.ALL,border=2)
        feature_box2.Add(cb5, proportion=0,flag=wx.EXPAND     #3gp
                      |wx.ALL,border=2)
        feature_box2.Add(cb6, proportion=0,flag=wx.EXPAND     #avi
                      |wx.ALL,border=2)

        #Third set of boxes vertically
        feature_box3 = wx.BoxSizer(wx.VERTICAL)
        feature_box3.Add(cb7, proportion=0,flag=wx.EXPAND     #flv
                      |wx.ALL,border=2)
        feature_box3.Add(cb8, proportion=0,flag=wx.EXPAND     #mp3
                      |wx.ALL,border=2)
        #--------------------------------------------------------------------------
        
        #-------------------
        #Extra feature boxes
        #-------------------
        #container for regex text box and filter button
        regex_box = wx.FlexGridSizer(cols=3, vgap=10, hgap=3)
        regex_box.Add(regex,proportion=0,flag=wx.TOP,border=7)
        regex_box.Add(self.regex,proportion=1,flag=wx.BOTTOM|wx.LEFT|wx.EXPAND,border=5)
        regex_box.Add(filter_btn,proportion=0,flag=wx.ALL,border=5)

        #container for (regex,filter) container and count text box
        feature_box4 = wx.BoxSizer(wx.VERTICAL)
        feature_box4.Add(self.count,proportion=1,flag=wx.TOP,border=5)
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
        prog_box.Add(self.progress,proportion=1,
                     flag=wx.ALL|wx.EXPAND,border=5)
        prog_box.Add(download_btn,proportion=0,border=5,
                     flag=wx.RIGHT|wx.TOP|wx.BOTTOM)

        #--------------------------------------------------------------------------      
        #container for introsizer and Containers #1,#2,#3,#4,#5
        #-------------------------------------------
        main_container = wx.BoxSizer(wx.VERTICAL)
        main_container.Add(self.introsizer,proportion = 0,flag=wx.EXPAND)
        main_container.Add(url_box,proportion = 0,flag=wx.EXPAND)
        main_container.Add(dir_box,proportion = 0,flag=wx.EXPAND)
        main_container.Add(Static_box,proportion = 1,
                           flag=wx.EXPAND)
        main_container.Add(feature_box,proportion = 0)
        main_container.Add(prog_box,proportion=0,flag=wx.EXPAND)
        
        panel.SetSizer(main_container)
        #--------------------------------------------------------------------------
        
        #an empty list for showing filtered links.
        self.filtered = []
        #for keeping track of old regex filtered list; used in (filter)
        self.old_filtered = []
        #List for checked links to download;
         #used in (enter),(filter),(EvtCheckBox)
        self.toDownload = []
        
    #--------------------------------------------------------------------------
    def EvtCheckBox(self, event):
        check_box = event.GetEventObject()
        regex = '.*.'+check_box.GetLabelText()                       #creating a regex pattern based on
                                                                      #the label str of selected checkbox.
            
        pattern = re.compile(regex)
        filtered = re.findall(regex, '\n'.join(self.urls))

        if event.IsChecked():
            self.filtered.extend(filtered)

        if not event.IsChecked():
            for item in filtered:
                self.filtered.remove(item)

        if filtered:
            
            if self.check_list:
                self.check_list.Destroy()

            if self.filtered:
                self.check_list = wx.CheckListBox(self.panel, -1, (5,120),
                                                  (604,260),self.filtered,
                                                  style = wx.HSCROLL)

                self.count.SetLabelText("No. of links found: "+str(len(self.filtered)))
            else:
                self.check_list = wx.CheckListBox(self.panel, -1, (5,120),
                                                  (604,260),self.urls,
                                                  style = wx.HSCROLL)

                self.count.SetLabelText("No. of links found: "+str(len(self.urls)))

            #Adding the list box to container
            self.bsizer.Add(self.check_list,proportion=1,flag=wx.EXPAND       
                  |wx.ALL,border=5 
                  )

        self.toDownload = []            
        self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox) 
        self.check_list.SetSelection(0)            
            
    #--------------------------------------------------------------------------
    def enter(self, event):
        '''
        The function to prepare a list of all urls found on home page,
        It works on text_enter_event of textctrl box called 'url'.
        '''

        home_url = self.url_field.GetValue()
        if home_url == "":
            self.url_field.SetValue("Please enter url")
            return
        error, self.urls = get_urls.main(home_url)
        if self.urls:
            try:
                self.info.Dismiss()
            except:
                pass
            try:
                self.check_list.Destroy()
                self.filtered = []
            except:
                pass

            self.check_list = wx.CheckListBox(self.panel, -1, (5,120),
                                              (604,260),self.urls,
                                              style = wx.HSCROLL)
            self.count.SetLabelText("No. of links found: "+str(len(self.urls)))
            
            self.bsizer.Add(self.check_list,proportion=1,flag=wx.EXPAND
                      |wx.ALL,border=5
                      )

            self.toDownload = []
            self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox)
            
    #--------------------------------------------------------------------------
    def filter(self,event):
        '''
        The function filters links found on the page.
        It uses regex to filter and display a list of urls matching the pattern.
        The pattern is specified in the box called regex.
        '''

        pattern = self.regex.GetValue()
        if self.urls:

            if pattern:
                pattern = re.compile(pattern)
                filtered = re.findall(pattern,'\n'.join(self.urls))
                self.filtered.extend(filtered)
                self.old_filtered = filtered

            else:
                for item in self.old_filtered:
                    self.filtered.remove(item)

            if self.check_list:
                self.check_list.Destroy()                                      #Destroying old list

            if self.filtered:    
                self.check_list = wx.CheckListBox(self.panel, -1, (5,120),         #creating new filtered list
                                                  (604,260),self.filtered,
                                                  style = wx.HSCROLL)
                self.count.SetLabelText("No. of links found: "+str(len(self.filtered)))
            else:
                self.check_list = wx.CheckListBox(self.panel, -1, (5,120),
                                                  (604,260),self.urls,
                                                  style = wx.HSCROLL)
                self.count.SetLabelText("No. of links found: "+str(len(self.urls)))

            self.bsizer.Add(self.check_list,proportion=1,flag=wx.EXPAND         #Adding the list box to container
                  |wx.ALL,border=5 
                  )

            #list of selected links
            self.toDownload = []
            
            self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox) 
            self.check_list.SetSelection(0)

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
            self.toDownload.append(string_at_index)
            status = ''
            self.check_list.SetSelection(index)                             #so that (un)checking also selects (moves the highlight)
            
        if not self.check_list.IsChecked(index):
            self.toDownload.remove(string_at_index)
            self.check_list.SetSelection(0)

        #print self.toDownload

    #--------------------------------------------------------------------------
    def download(self,event):
        '''
        The function is bind with download button and download the content.
        It fetches urls from the 'contents' textctrl and sends urls to
        downloader_script.
        Uses 'browse' filedialogs current path to save files.
        '''
        urls_to_download = self.toDownload
        try:
            error = downloader_script.main(urls_to_download,self.path)
            if error:
                self.progress.SetValue(error)
    
        except AttributeError:
            self.dir.SetValue(os.curdir)
            self.path = os.curdir

##        max = 50
##
##        self.progress = wx.ProgressDialog("Progress dialog example",
##                               "Downloading...",
##                               maximum = max,
##                               parent=self.panel,
##                               style = 0
##                                | wx.PD_APP_MODAL
##                                | wx.PD_CAN_ABORT
##                                #| wx.PD_CAN_SKIP
##                                #| wx.PD_ELAPSED_TIME
##                                | wx.PD_ESTIMATED_TIME
##                                | wx.PD_REMAINING_TIME
##                                #| wx.PD_AUTO_HIDE
##                                )
##
##        keepGoing = True
##        count = 0
##
##        while keepGoing and count < max:
##            count += 1
##            wx.MilliSleep(10)
##            wx.Yield()
##            
##            if count >= max / 2:
##                (keepGoing, skip) = self.progress.Update(count)
##            else:
##                (keepGoing, skip) = self.progress.Update(count)
##
##                
##        self.progress.Destroy()

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
            print('You selected: %s\n' % dlg.GetPath())
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
        self.count.SetLabelText(" ")

    #--------------------------------------------------------------------------
    def close(self,event):
        '''
        Destroys the window object.   
        '''
        self.win.Destroy()

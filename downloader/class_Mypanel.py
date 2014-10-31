'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This is the Mypanel class for GUI module.
It creates the buttons and packs them into box.
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
    -cancel
    -filter
    -EvtCheckListBox
    -close
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required modules"""
import wx
import get_urls,downloader_script
import re

class Mypanel(object):
    def __init__(self,bkg,win):
        self.win = win
        self.bkg = bkg
        
        #creating buttons
        download_btn = wx.Button(bkg,label = "download",size=(80,25))
        download_btn.Bind(wx.EVT_BUTTON,self.download)

        browse_btn = wx.Button(bkg,label = "browse",size=(80,25))
        browse_btn.Bind(wx.EVT_BUTTON,self.browse)

        cancel_btn = wx.Button(bkg,label = "cancel",size=(80,25))
        cancel_btn.Bind(wx.EVT_BUTTON,self.cancel)

        clsbtn = wx.Button(bkg,label = "CLOSE",size=(80,25))
        clsbtn.Bind(wx.EVT_BUTTON,self.close)

        fbtn = wx.Button(bkg,label="Filter",size=(80,25))
        fbtn.Bind(wx.EVT_BUTTON,self.filter)

        #--------------------------------------------------------------------------
        #defining text areas; to input text
        
        self.url = wx.TextCtrl(bkg,size=(390,25),pos=(5,5),
                               style=wx.TE_PROCESS_ENTER)
        self.url.Bind(wx.EVT_TEXT_ENTER, self.enter)
        self.dir = wx.TextCtrl(bkg,size=(390,25),pos=(5,30))
        self.contents = wx.TextCtrl(bkg,style = wx.TE_MULTILINE|wx.HSCROLL,
                                   size=(100,245)
                                    )

        self.count = wx.TextCtrl(bkg,size=(255,25),pos=(420,295))
        self.regex = wx.TextCtrl(bkg,size=(255,25),pos=(420,310))
        self.progress = wx.TextCtrl(bkg,size=(390,25),pos=(5,335))

        #--------------------------------------------------------------------------
        #Adding CheckBoxes

        cb1 = wx.CheckBox(bkg, -1, "jpeg",
                          (5, 295), (75, 25))
        cb2 = wx.CheckBox(bkg, -1, "png",
                          (5, 310), (75, 25))
        cb3 = wx.CheckBox(bkg, -1, "gif",
                          (5, 335), (75, 25))
        cb4 = wx.CheckBox(bkg, -1, "mp4",
                          (35, 295), (75, 25))
        cb5 = wx.CheckBox(bkg, -1, "3gp",
                          (35,310), (75, 25))
        cb6 = wx.CheckBox(bkg, -1, "avi",
                          (35, 335), (75, 25))
        cb7 = wx.CheckBox(bkg, -1, "flv",
                          (70, 295), (75, 25))
        cb8 = wx.CheckBox(bkg, -1, "mp3",
                          (70, 310), (75, 25))

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
        #The text controls
        vbox11 = wx.BoxSizer(wx.VERTICAL)
        vbox11.Add(self.url,proportion=0,flag=wx.ALL|wx.EXPAND,border=5)
        vbox11.Add(self.dir,proportion=0,flag=wx.ALL|wx.EXPAND,border=5)
        vbox11.Add(self.contents,proportion=1,flag=wx.TE_MULTILINE
                  |wx.EXPAND
                  |wx.ALL,border=5
                  )
        self.vbox11 = vbox11

        #The checkBoxes        
        vbox12 = wx.BoxSizer(wx.VERTICAL)
        
        vbox12.Add(cb1, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)
        vbox12.Add(cb2, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)
        vbox12.Add(cb3, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)

        vbox13 = wx.BoxSizer(wx.VERTICAL)
        vbox13.Add(cb4, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)
        vbox13.Add(cb5, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)
        vbox13.Add(cb6, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)

        vbox14 = wx.BoxSizer(wx.VERTICAL)
        vbox14.Add(cb7, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)
        vbox14.Add(cb8, proportion=0,flag=wx.EXPAND
                      |wx.ALL,border=2)

        #--------------------------------------------------------------------------
        #Extra feature boxes
        vbox15 = wx.BoxSizer(wx.VERTICAL)
        vbox15.Add(self.count,proportion=1,flag=wx.ALL|wx.EXPAND,border=3)
        vbox15.Add(self.regex,proportion=1,flag=wx.ALL|wx.EXPAND,border=3)
        vbox15.Add(fbtn,proportion=0,flag=wx.LEFT,border=178)

        #--------------------------------------------------------------------------
        #All vertical boxes in horizontal box
        hbox1 = wx.BoxSizer()
        hbox1.Add(vbox12,proportion=0,flag=wx.EXPAND)
        hbox1.Add(vbox13,proportion=0,flag=wx.EXPAND)
        hbox1.Add(vbox14,proportion=0,flag=wx.EXPAND)
        hbox1.Add(vbox15,proportion=0)

        #The two vertical boxes in one
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(vbox11,proportion=1,flag=wx.EXPAND)
        vbox1.Add(hbox1,proportion=0,flag=wx.EXPAND)
        vbox1.Add(self.progress,proportion=0,flag=wx.ALL|wx.EXPAND,border=5)
        
        #--------------------------------------------------------------------------
        #Buttons
        vbox21 = wx.BoxSizer(wx.VERTICAL)
        vbox21.Add(download_btn,proportion=0,border=5,flag=wx.TOP)
        vbox21.Add(browse_btn,proportion=0,border=10,flag=wx.TOP)
        vbox21.Add(cancel_btn,proportion=0,border=10,flag=wx.TOP)

        #Close button
        vbox22 = wx.BoxSizer(wx.VERTICAL)
        vbox22.Add(clsbtn,proportion=0,border=5,flag=wx.RIGHT|wx.TOP|wx.BOTTOM)

        #The two vertical boxes in single one.
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(vbox21,proportion=1,flag=wx.EXPAND)
        vbox2.Add(vbox22,proportion=0)

        #--------------------------------------------------------------------------      
        #Vertical boxes into horizontal hbox.  
        hbox = wx.BoxSizer()
        hbox.Add(vbox1,proportion = 1,flag = wx.EXPAND|wx.BOTTOM)
        hbox.Add(vbox2,proportion = 0,flag = wx.EXPAND,border = 5)

        bkg.SetSizer(hbox)

        #an empty list for checkbox filter.
        self.filtered = []
        #for keeping track of old regex filtered list
        self.old_filtered = []
        
    #--------------------------------------------------------------------------
    def EvtCheckBox(self, event):
        check_box = event.GetEventObject()
        regex = '.*.'+check_box.GetLabelText()                          #creating a regex pattern based on
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
                self.check_list = wx.CheckListBox(self.bkg, -1, (5,75),
                                                  (488,245),self.filtered,
                                                  style = wx.HSCROLL)

                self.count.SetValue("No. of links found: "+str(len(self.filtered)))
            else:
                self.check_list = wx.CheckListBox(self.bkg, -1, (5,75),
                                                  (488,245),self.urls,
                                                  style = wx.HSCROLL)

                self.count.SetValue("No. of links found: "+str(len(self.urls)))

            self.vbox11.Add(self.check_list,proportion=1,flag=wx.EXPAND      #Adding the list box to container
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
        error, self.urls = get_urls.main(self.url.GetValue())
        if self.urls:

            #destroying the contents box, so as to put the checklist inplace.
            if self.contents:
                self.contents.Destroy()

            try:
                self.check_list.Destroy()
                self.filtered = []
            except:
                pass

            self.check_list = wx.CheckListBox(self.bkg, -1, (5,75),
                                              (488,245),self.urls,
                                              style = wx.HSCROLL)
            self.count.SetValue("No. of links found: "+str(len(self.urls)))
            
            self.vbox11.Add(self.check_list,proportion=1,flag=wx.EXPAND
                      |wx.ALL,border=5
                      )

            self.toDownload = []
            self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox)
            
            #setting the count of links

        else:
            self.contents.SetValue(error)


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
            self.dir.SetValue("Please select a location")

##        max = 50
##
##        self.progress = wx.ProgressDialog("Progress dialog example",
##                               "Downloading...",
##                               maximum = max,
##                               parent=self.bkg,
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
    def cancel(self,event):
        '''
        This is bound to cancel button, when pressed, it clears all text areas.
        '''
        self.url.SetValue(" ")
        try:
            self.check_list.Destroy()
        except Exception:
            pass
        self.regex.SetValue(" ")
        self.count.SetValue(" ")
        self.contents = wx.TextCtrl(self.bkg,style = wx.TE_MULTILINE|wx.HSCROLL,
                                   size=(100,245)
                                    )
        self.vbox11.Add(self.contents,proportion=1,flag=wx.TE_MULTILINE
                       |wx.EXPAND
                       |wx.ALL,border=5
                       )
        self.contents.SetValue(" ")

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
                self.check_list = wx.CheckListBox(self.bkg, -1, (5,75),         #creating new filtered list
                                                  (488,245),self.filtered,
                                                  style = wx.HSCROLL)
                self.count.SetValue("No. of links found: "+str(len(self.filtered)))
            else:
                self.check_list = wx.CheckListBox(self.bkg, -1, (5,75),
                                                  (488,245),self.urls,
                                                  style = wx.HSCROLL)
                self.count.SetValue("No. of links found: "+str(len(self.urls)))

            self.vbox11.Add(self.check_list,proportion=1,flag=wx.EXPAND         #Adding the list box to container
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
    def close(self,event):
        '''
        Destroys the window object.   
        '''
        self.win.Destroy()

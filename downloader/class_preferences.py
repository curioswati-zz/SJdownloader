'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This is the preference class for open_pref function defined in class FlatMenu.
It creates the widgets like buttons and textAreas; packs them into container.
It also implements the binding of buttons to various events using functions to
browse location, save or cancel changes.

It imports:
    -wx
It defines:
    -__init__
    -browse
    -save
    -close
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required Modules"""
import wx
from wx.lib.agw import aquabutton as AB

class open_pref(object):
        
    def __init__(self,win,panel):
        self.win = win
        self.panel = panel
        self.DD = '.'

        self.panel.SetBackgroundColour((198,222,223,255))
        self.panel.SetForegroundColour((60,60,60,255))
        #---------------------------------------------------------------
        #Creating widgets for window
        #Buttons
        savebtn = AB.AquaButton(self.panel, -1, None,
                                "Save",size=(60,30))
        savebtn.SetBackgroundColour((198,222,223,255))
        savebtn.SetForegroundColour("Black")
        savebtn.SetToolTipString("Save changes")
        savebtn.Bind(wx.EVT_BUTTON, self.save)
        
        cancelbtn = AB.AquaButton(self.panel, -1, None,
                                  "Cancel",size=(60,30))
        cancelbtn.SetBackgroundColour((198,222,223,255))
        cancelbtn.SetForegroundColour("Black")
        cancelbtn.SetToolTipString("Click to show found links")
        cancelbtn.Bind(wx.EVT_BUTTON, self.cancel)

        browse_btn = wx.BitmapButton(self.panel, -1, wx.Bitmap('../Icons/folder.png'))
        browse_btn.SetBackgroundColour((198,222,223,255))
        browse_btn.SetForegroundColour("Black")
        browse_btn.SetToolTipString("Select location")
        browse_btn.Bind(wx.EVT_BUTTON,self.browse)
        
        #--------------------------------------------------------------  
        #static label
        location = wx.StaticText(self.panel, -1, "Choose default directory")
        filterLabel  = wx.StaticText(self.panel, -1, "Choose default filters",
                                 size=(200,25))
        
        #default dir location
        self.dir = wx.TextCtrl(self.panel,size=(200,25))
        self.dir.SetToolTipString("Selected default location");
        
        #Filters list
        self.filter_list = ['.*.jpg','.*.png',
                       '/\.(?:z(?:ip|[0-9]{2})|r(?:ar|[0-9]{2})|jar|bz2|gz|tar|rpm|7z(?:ip)?|lzma|xz)$/i',
                       '/\.(?:mp3|wav|og(?:g|a)|flac|midi?|rm|aac|wma|mka|ape)$/i',
                       '/\.(?:exe|msi|dmg|bin|xpi|iso)$/i',
                       '/\.(?:pdf|xlsx?|docx?|odf|odt|rtf)$/i',
                       '/\.(?:jp(?:e?g|e|2)|gif|png|tiff?|bmp|ico)$/i',
                       '/\.(?:mpeg|ra?m|avi|mp(?:g|e|4)|mov|divx|asf|qt|wmv|m\dv|rv|vob|asx|ogm|ogv|webm)$/i']
        self.filter_list_box = wx.CheckListBox(self.panel,-1,(10,60),
                                           (380,200),self.filter_list,style=wx.HSCROLL)

        #checkbox for applying all
        self.applyAll = wx.CheckBox(self.panel, -1, "apply all",
                                    (70, 310), (85, 20))
        self.applyAll.Bind(wx.EVT_CHECKBOX,self.apply_all)
        #------------------------------------------------------------------
        #Wrapping the boxes
        
        #for dir controls
        dir_box = wx.BoxSizer()
        dir_box.Add(location,proportion=0,flag=wx.ALL,border=5)
        dir_box.Add(self.dir,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        dir_box.Add(browse_btn,proportion=0,border=5,flag=wx.ALL)

        #--------------------------------------------------------------------
        #Label box
        labels = wx.BoxSizer()
        labels.Add(filterLabel,proportion=1)
        labels.Add(self.applyAll,proportion=1)

        #--------------------------------------------------------------------
        #For filter controls
        filter_box = wx.BoxSizer()
        filter_box.Add(self.filter_list_box,proportion=1,flag=wx.EXPAND)

        #Button container
        button_cont = wx.BoxSizer(wx.VERTICAL)
        button_cont.Add(savebtn,proportion=0,flag=wx.TOP,border=190)
        button_cont.Add(cancelbtn,proportion=0,flag=wx.ALL,border=2)
        
        #option container
        self.options = wx.BoxSizer(wx.VERTICAL)
        self.options.Add(dir_box,proportion=0)
        self.options.Add(labels,proportion=0,flag=wx.ALL,border=5)
        self.options.Add(filter_box, proportion=1)

        #Main_container
        self.main_container = wx.BoxSizer()
        self.main_container.Add(self.options,proportion=1,flag=wx.EXPAND)
        self.main_container.Add(button_cont,proportion=0,
                                flag=wx.ALL|wx.EXPAND,border=5)

        self.panel.SetSizer(self.main_container)
        self.panel.Layout()

    #-------------------------------------------------------------------
    def apply_all(self, event):
        if event.IsChecked():
            try:
                indices = range(len(self.filter_list))
                self.filter_list_box.SetChecked(indices)
            except Exception as e:
                     print e
        else:
            try:
                for index in xrange(len(self.filter_list)):
                    self.filter_list_box.Check(index,False)
            except Exception as e:
                print e
    #-------------------------------------------------------------------
    def browse(self, event):
        '''
        The function is bind with the browse button.
        It opens a directory location, and set it as default
        '''
        dir_= self.dir.GetValue()
        dlg = wx.DirDialog(self.win, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           | wx.DD_CHANGE_DIR
                           )

        dlg.SetPath(dir_)
        if dlg.ShowModal() == wx.ID_OK:
            self.DD = dlg.GetPath()
            self.dir.SetValue(self.DD)

        dlg.Destroy()
            
    #-------------------------------------------------------------------    
    def save(self, event):
        '''
        The function is bind with the save button.
        It saves all the changes in preferences.
        '''
        dir_file = open('default_dir.txt','w')
        print self.DD
        dir_file.write(self.DD)
        dir_file.close()

        self.panel.Close()
        self.win.Destroy()
    #-------------------------------------------------------------------    
    def cancel(self, event):
        '''
        The function is bind with the save button.
        It saves all the changes in preferences.
        '''
        
        self.panel.Close()
    

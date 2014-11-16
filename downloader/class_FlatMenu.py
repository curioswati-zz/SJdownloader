'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The Menu class for class_Mypanel.
It creates a menubar.
The methods defined inside the class are menu item events,that
occurs when an item is clicked. Method names themselves reflect their function.

It imports:
    -wx
    -os
    -sys
It defines:
    -__init__
    -New
    -Save
    -Exit
    -Pref
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required Modules"""
import wx
import os, sys
from wx.lib.agw import aquabutton as AB
#from class_FM import FM_MyRenderer

#Linking to icons path.
#----------------------------------------------------------
try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

iconsDir = os.path.join(dirName, 'Icons')
sys.path.append(os.path.split(dirName)[0])
#----------------------------------------------------------

class Menu():
    
    default_dir = '.'
    
    def __init__(self,win):
        self.win = win

        #Creating a new window frame        
        win = wx.Frame(self.win)
        #The menubar
        menubar = wx.MenuBar()

        #Creating menu items
        #---------------------------------------------------------------------
        fileMenu = wx.Menu()
        new = fileMenu.Append(101, '&New\tCtrl+N', 'New file')
        save = fileMenu.Append(102, '&Save\tCtrl+S', 'Save file')
        close = fileMenu.Append(103, '&Exit\tCtrl+X', 'exit')
        menubar.Append(fileMenu, '&File')

        editMenu = wx.Menu()
        pref = editMenu.Append(104, '&Preferences\tCtrl+E', 'settings')
        menubar.Append(editMenu, '&Edit')

        self.win.SetMenuBar(menubar)

        #Binding events with menu items
        #---------------------------------------------------------------------
        self.win.Bind(wx.EVT_MENU, self.New, new, id=101)
        self.win.Bind(wx.EVT_MENU, self.Save, id=102)
        self.win.Bind(wx.EVT_MENU, self.Exit, id=103)
        self.win.Bind(wx.EVT_MENU, self.Pref, pref)
    #---------------------------------------------------------------------
    def New(self, event):
        print "FileMenu"

    #---------------------------------------------------------------------
    def Save(self, event):

        #The save file dialog
        dlg = wx.FileDialog(
            self.win, message="Save file in", defaultDir=os.getcwd(), 
            defaultFile="", wildcard='', style=wx.SAVE
            )
        
        # This sets the default filter that the user will initially see. Otherwise,
         # the first filter in the list will be used by default.
        dlg.SetFilterIndex(2)

        # Show the dialog and retrieve the user response.
         #If it is the OK response,process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

        dlg.Destroy()

    #---------------------------------------------------------------------
    def Pref(self, event):
        win = open_pref()

    #---------------------------------------------------------------------
    def Exit(self, event):
        self.win.Destroy()

class open_pref():
    def __init__(self):
        app = wx.App()
        self.win = wx.Frame(None, title='Preferences',size=(500,350),
                            pos = (300,200))
        self.panel = wx.Panel(self.win)
        self.panel.SetBackgroundColour((198,222,223,255))
        self.panel.SetForegroundColour((60,60,60,255))
        
        #---------------------------------------------------------------
        #Creating widgets for window
        
        #Buttons
        savebtn = AB.AquaButton(self.panel, -1, None,
                                "Save",size=(80,30),pos = (415,280))
        savebtn.SetBackgroundColour((198,222,223,255))
        savebtn.SetForegroundColour("Black")
        savebtn.SetToolTipString("Save changes")
        savebtn.Bind(wx.EVT_BUTTON, self.save)
        
        cancelbtn = AB.AquaButton(self.panel, -1, None,
                                  "Cancel",size=(80,30),pos = (415,315))
        cancelbtn.SetBackgroundColour((198,222,223,255))
        cancelbtn.SetForegroundColour("Black")
        cancelbtn.SetToolTipString("Click to show found links")
        cancelbtn.Bind(wx.EVT_BUTTON, self.cancel)
        
        #options
        #default dir location
        self.dir = wx.TextCtrl(self.panel,size=(300,25))
        self.dir.SetToolTipString("Selected default location");
        
        browse_btn = wx.BitmapButton(self.panel, -1, wx.Bitmap('../Icons/folder.png'))
        browse_btn.SetBackgroundColour((198,222,223,255))
        browse_btn.SetForegroundColour("Black")
        browse_btn.SetToolTipString("Select location")
        browse_btn.Bind(wx.EVT_BUTTON,self.browse)
        
        #---------------------------------------------------------------
        #static label
        location = wx.StaticText(self.panel, -1, "Choose default directory")
        filters  = wx.StaticText(self.panel, -1, "Choose default filters")                                  
        #---------------------------------------------------------------
        #Wrapping the boxes
        
        #for dir controls
        dir_box = wx.BoxSizer()
        dir_box.Add(location,proportion=0,flag=wx.ALL,border=5)
        dir_box.Add(self.dir,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        dir_box.Add(browse_btn,proportion=0,border=5,flag=wx.ALL)
        #--------------------------------------------------------------

        #Button container
        button_cont = wx.BoxSizer(wx.VERTICAL)
        button_cont.Add(savebtn,proportion=0,flag=wx.ALL,border=2)
        button_cont.Add(cancelbtn,proportion=0,flag=wx.ALL,border=2)
        
        #option container
        self.options = wx.BoxSizer()
        self.options.Add(dir_box,proportion=1,flag=wx.EXPAND)

        #Main_container
        self.main_container = wx.BoxSizer()
        self.main_container.Add(self.options,proportion=1,
                                flag=wx.ALL,border=5)
        self.main_container.Add(button_cont,proportion=0,
                                flag=wx.ALL,border=5)
                                
        #---------------------------------------------------------------
        self.win.Show()
        app.MainLoop()
        
    #------------------------------------------------------------------- 
    def browse():
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
            default_dir = dlg.GetPath()

        dlg.Destroy()
    #-------------------------------------------------------------------
    def save(self, event):
        '''
        The function is bind with the save button.
        It saves all the changes in preferences.
        '''

        self.win.Destroy()
        
    #-------------------------------------------------------------------    
    def cancel(self, event):
        '''
        The function is bind with the save button.
        It saves all the changes in preferences.
        '''

        self.win.Destroy()
        
    

    

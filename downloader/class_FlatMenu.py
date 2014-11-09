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
        self.win = wx.Frame(None, title='Preferences',size=(500,350))
        self.panel = wx.Panel(self.win)
        self.panel.SetBackgroundColour((198,222,223,255))
        self.panel.SetForegroundColour((60,60,60,255))

        #Creating widgets for window
        #sub_containers
        self.box = wx.StaticBox(self.panel, -1,size=(400,300))
        self.options = wx.BoxSizer()
        self.options.Add(self.box,proportion=1,flag=wx.EXPAND)

        #Button container
        #self.button_cont = wx.BoxSizer(wx.VERTICAL)
        savebtn = AB.AquaButton(self.panel, -1, None,
                                "Save",size=(80,30))
        #cancelbtn = AB.AquaButton(self.panel, -1, None,
         #                         "Cancel",size=(80,30))
        #self.button_cont.Add(savebtn,proportion=0,flag=wx.TOP,border=150)
        #self.button_cont.Add(cancelbtn,proportion=0,flag=wx.ALL,border=5)

        #Main_container
        self.main_container = wx.BoxSizer()
        self.main_container.Add(self.options,proportion=1,
                                flag=wx.ALL,border=5)
        self.main_container.Add(savebtn,proportion=0,
                                flag=wx.ALL,border=5)
        self.win.Show()
        app.MainLoop()
        
    

    

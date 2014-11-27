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
import class_preferences

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
        open_pref()

    #---------------------------------------------------------------------
    def Exit(self, event):
        self.win.Destroy()
        
#-------------------------------------------------------------------------        

def open_pref():
    '''
    main function for preferences window
    '''
    app = wx.App()

    #window object
    window = wx.Frame(None,title = "Preferences",size=(500,400))

    #box object
    bkg = wx.Panel(window)
    bkg.SetBackgroundColour((198,222,223,255))
    bkg.SetForegroundColour((60,60,60,255))

    #packing the box
    class_preferences.open_pref(window,bkg)

    #show the window
    window.Show()

    #execute the loop for maintaining the window
    app.MainLoop()

#--------------------------------------------------------------------------

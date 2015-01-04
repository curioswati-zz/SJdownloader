'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The script is used by Mypanel class to create menubar using the Menu class
defined here.

It imports:
    -wx
    -os
    -sys
    -class_preferences
    -class_downloads
    -class_Mypanel
It defines:
    -__init__
    -New
    -Save
    -Exit
    -Pref
    -History
    -Downloads
    -About
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required Modules"""
import wx
import os
import sys

import class_preferences
import class_downloads
import class_Mypanel

#---------------------------------------------------------------------------------
class Menu():
    '''
    The Menu class for creating menu.
    The methods defined inside the class are menu item events,that
    occurs when an item is clicked. Method names themselves reflect their function.
    '''
    
    def __init__(self,win):
        self.win = win

        #The menubar
        menubar = wx.MenuBar()

        #-------------------------Creating menu items-------------------------
        fileMenu = wx.Menu()
        new = fileMenu.Append(101, '&New\tCtrl+N', 'New file')
        save = fileMenu.Append(102, '&Save\tCtrl+S', 'Save file')
        close = fileMenu.Append(103, 'E&xit\tCtrl+X', 'exit')
        menubar.Append(fileMenu, '&File')

        editMenu = wx.Menu()
        pref = editMenu.Append(104, '&Preferences\tCtrl+p', 'settings')
        menubar.Append(editMenu, '&Edit')

        viewMenu = wx.Menu()
        history = viewMenu.Append(105, '&History\tCtrl+h', 'history')
        downloads = viewMenu.Append(196, '&Downloads\tCtrl+d', 'downloads')
        menubar.Append(viewMenu, '&View')

        helpMenu = wx.Menu()
        about = helpMenu.Append(106, '&About\tCtrl+a','about')
        menubar.Append(helpMenu, '&Help')

        self.win.SetMenuBar(menubar)

        #------------------Binding events with menu items---------------------
        self.win.Bind(wx.EVT_MENU, self.New, new, id=101)
        self.win.Bind(wx.EVT_MENU, self.Save, id=102)
        self.win.Bind(wx.EVT_MENU, self.Exit, id=103)
        self.win.Bind(wx.EVT_MENU, self.Pref, pref)
        self.win.Bind(wx.EVT_MENU, self.History, history)
        self.win.Bind(wx.EVT_MENU, self.Downloads, downloads)
        self.win.Bind(wx.EVT_MENU, self.About, about)
    #-----------------------------------------------------------------------------
    def New(self, event):
        '''
        Method fired on new item of file menu.
        Creates a new instance of gui window.
        '''
        #window object
        win = wx.Frame(None,title = "SJdownloader",
                       size=(575,420))
        panel = wx.Panel(win)
        class_Mypanel.Mypanel(panel,win)
        win.Show()

    #-----------------------------------------------------------------------------
    def Save(self, event):
        '''
        Method fired on save item of file menu.
        '''
        #currently the method has no significant use.
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

    #-----------------------------------------------------------------------------
    def Exit(self, event):
        '''
        Method fired on exit item of file menu
        '''
        self.win.Destroy()

    #-----------------------------------------------------------------------------
    def Pref(self, event):
        '''
        Method fired on preferences item of edit menu.
        Used to open preferences window.
        '''
        open_pref()

    #-----------------------------------------------------------------------------
    def History(self, event):
        '''
        Method fired on history item of view menu.
        Currently using preferences window to show hsitory.
        '''
        open_pref()

    #-----------------------------------------------------------------------------
    def Downloads(self, event):
        '''
        Method fired on downloads item of view menu.
        used to open downloads window.
        '''
        open_downloads()

    #-----------------------------------------------------------------------------
    def About(self, event):
        '''
        Method fired on about item of help menu.
        '''
        #currently not implemented.
        about_dl()
        
#---------------------------------------------------------------------------------        
def open_pref():
    '''
    main function for preferences window
    '''
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
   
#---------------------------------------------------------------------------------  
def about_dl():
    pass

#---------------------------------------------------------------------------------        
# def open_history():
#     '''
#     main function for history window
#     '''
#     #currently not implemented.
#     #window object
#     window = wx.Frame(None,title = "History",size=(400,300))

#     #box object
#     bkg = wx.Panel(window)
#     bkg.SetBackgroundColour((198,222,223,255))
#     bkg.SetForegroundColour((60,60,60,255))

#     #packing the box
#     #class_preferences.open_pref(window,bkg)

#     #show the window
#     window.Show()

#---------------------------------------------------------------------------------        
def open_downloads():
    '''
    main function for downloads window
    '''
    #window object
    window = wx.Frame(None,title = "Downloads",size=(480,300))

    #box object
    bkg = wx.Panel(window)
    bkg.SetBackgroundColour((198,222,223,255))
    bkg.SetForegroundColour((60,60,60,255))

    #packing the box
    class_downloads.open_downloads(window,bkg)

    #show the window
    window.Show()

#---------------------------------------------------------------------------------        
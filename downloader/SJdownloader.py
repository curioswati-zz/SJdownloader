'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The downloader main module.
It creates a GUI window with the help of Mypanel class.
It import:
    -wx
    -Mypanel from class_Mypanel
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required modules"""
import wx
from class_Mypanel import Mypanel

#----------------------------------------------------------------------
def main():
    '''
    The main function which creates the window and box objects and uses
    Mypanel class for creating widgets and binding events.
    '''
    app = wx.App()

    #window object
    win = wx.Frame(None,title = "Downloader",size=(575,420))

    #box object
    bkg = wx.Panel(win)
    
    #packing the box
    Mypanel(bkg,win)

    #show the window
    win.Show()

    #execute the loop for maintaining the window
    app.MainLoop()

#----------------------------------------------------------------------
if __name__ == '__main__':
    main()

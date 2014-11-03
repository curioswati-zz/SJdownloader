"""
The downloader main module.
It creates a GUI window with the help of two classes.
It import:
    -wx
    -Mypanel    
"""
import wx
from class_Mypanel import Mypanel

def main():
    '''
    The main function which creates the window and box objects and uses
    Mypanel class for creating widgets and binding events.
    '''
    app = wx.App()

    #window object
    win = wx.Frame(None,title = "Downloader",size=(720,550))

    #box object
    bkg = wx.Panel(win)

    #packing the box
    Mypanel(bkg,win)

    #show the window
    win.Show()

    #execute the loop for maintaining the window
    app.MainLoop()

    #destroy window
    #win.Destroy()

if __name__ == '__main__':
    main()

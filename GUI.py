"""
The pdf converter main module.
It creates a GUI window with the help of two classes.
It import:
    -wx
    -Mypanel    
"""
import wx
from class_Mypanel import Mypanel

app = wx.App()

#window object
win = wx.Frame(None,title = "simple Editor",size=(500,400))

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

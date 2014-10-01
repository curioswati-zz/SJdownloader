'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''
This is the Mypanel class for download_win module.
It creates the buttons and packs them into box.
It also implements the fetching and conversion of the data using create_book.

It imports:
    -wx
    -create_book
It defines:
    -__init__
    -download
    -browse
    -cancel
    -close
''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required modules"""
import wx
import get_images

class Mypanel(object):
    def __init__(self,bkg,win):
        self.win = win
        
        #creating buttons
        self.download_btn = wx.Button(bkg,label = "download",size=(80,25))
        self.download_btn.Bind(wx.EVT_BUTTON,self.download)

        self.browse_btn = wx.Button(bkg,label = "browse",size=(80,25))
        self.browse_btn.Bind(wx.EVT_BUTTON,self.browse)

        self.cbtn = wx.Button(bkg,label = "cancel",size=(80,25))
        self.cbtn.Bind(wx.EVT_BUTTON,self.cancel)

        self.clsbtn = wx.Button(bkg,label = "CLOSE",size=(80,25))
        self.clsbtn.Bind(wx.EVT_BUTTON,self.close)

        #defining text areas; to input text
        self.url = wx.TextCtrl(bkg,size=(390,25),pos=(5,5))
        self.dir = wx.TextCtrl(bkg,size=(390,25),pos=(5,30))
        self.contents = wx.TextCtrl(bkg,style = wx.TE_MULTILINE|wx.HSCROLL,size=(300,325))

        #wrapping in the box
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.url,proportion=0,flag=wx.ALL|wx.EXPAND,border=5)
        vbox1.Add(self.dir,proportion=0,flag=wx.ALL|wx.EXPAND,border=5)
        vbox1.Add(self.contents,proportion=1,flag=wx.TE_MULTILINE|wx.EXPAND|wx.ALL,border=5)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.download_btn,proportion=0,border=5,flag=wx.TOP)
        vbox2.Add(self.browse_btn,proportion=0,border=10,flag=wx.TOP)
        vbox2.Add(self.cbtn,proportion=0,border=20,flag=wx.TOP)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(self.clsbtn,proportion=0,border=5,flag=wx.RIGHT|wx.TOP|wx.BOTTOM)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(vbox2,proportion=1,flag=wx.EXPAND)
        vbox.Add(vbox3,proportion=0)

        hbox = wx.BoxSizer()
        hbox.Add(vbox1,proportion = 1,flag = wx.EXPAND|wx.BOTTOM)
        hbox.Add(vbox,proportion = 0,flag = wx.EXPAND,border = 5)

        bkg.SetSizer(hbox)

    def download(self,event):
        url = self.url.GetValue()
        dir_= self.dir.GetValue()
        get_images.main(url,dir_)
        
    def browse(self,event):
        dialog = wx.FileDialog(self,self._defaultDirectory, "",wx.FD_OPEN|wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()
        dialog.Destroy()
        
    def cancel(self,event):
        self.url.SetValue(" ")
        self.contents.SetValue(" ")
        
    def close(self,event):
        self.win.Destroy()
       
      
                

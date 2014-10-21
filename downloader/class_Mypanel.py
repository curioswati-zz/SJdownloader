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
    -download
    -filter
    -browse
    -cancel
    -close
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required modules"""
import wx
import get_urls,downloader_script
import re

class Mypanel(object):
    def __init__(self,bkg,win):
        self.win = win
        
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

        #defining text areas; to input text
        self.url = wx.TextCtrl(bkg,size=(390,25),pos=(5,5))
        self.dir = wx.TextCtrl(bkg,size=(390,25),pos=(5,30))
        self.contents = wx.TextCtrl(bkg,style = wx.TE_MULTILINE|wx.HSCROLL,
                                   size=(300,325)
                                    )
        self.regex = wx.TextCtrl(bkg,size=(390,25),pos=(5,355))

        #wrapping in the box
        #The text controls
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.url,proportion=0,flag=wx.ALL|wx.EXPAND,border=5)
        vbox1.Add(self.dir,proportion=0,flag=wx.ALL|wx.EXPAND,border=5)
        vbox1.Add(self.contents,proportion=1,flag=wx.TE_MULTILINE
                  |wx.EXPAND
                  |wx.ALL,border=5
                  )

        hbox1 = wx.BoxSizer()
        hbox1.Add(self.regex,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        hbox1.Add(fbtn,proportion=0,flag=wx.ALL,border=5)

        vbox1.Add(hbox1,proportion=0,flag=wx.TOP|wx.EXPAND)

        #Buttons
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(download_btn,proportion=0,border=5,flag=wx.TOP)
        vbox2.Add(browse_btn,proportion=0,border=10,flag=wx.TOP)
        vbox2.Add(cancel_btn,proportion=0,border=10,flag=wx.TOP)

        #Close button
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(clsbtn,proportion=0,border=5,flag=wx.RIGHT|wx.TOP|wx.BOTTOM)

        #wrapping vertical boxes into single vbox.
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(vbox2,proportion=1,flag=wx.EXPAND)
        vbox.Add(vbox3,proportion=0)

        #wrapping vertical boxes into horizontal hbox.  
        hbox = wx.BoxSizer()
        hbox.Add(vbox1,proportion = 1,flag = wx.EXPAND|wx.BOTTOM)
        hbox.Add(vbox,proportion = 0,flag = wx.EXPAND,border = 5)

        bkg.SetSizer(hbox)

    #--------------------------------------------------------------------------
    def download(self,event):
        '''
        The function is bind with download button and download the content.
        It fetches urls from the 'contents' textctrl and sends urls to
        downloader_script.
        Uses 'browse' filedialogs current path to save files.
        '''
        urls_to_download = self.contents.GetValue().split('\n')
        try:
            downloader_script.main(urls_to_download,self.path)
        except AttributeError:
            print "Please select a location"

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

        dlg.Destroy()
        self.dir.SetValue(self.path)
        
    #--------------------------------------------------------------------------
    def cancel(self,event):
        '''
        This is bound to cancel button, when pressed, it clears all text areas.
        '''
        self.url.SetValue(" ")
        self.contents.SetValue(" ")

    #--------------------------------------------------------------------------
    def filter(self,event):
        '''
        The function filters links found on the page.
        It uses regex to filter and display a list of urls matching the pattern.
        The pattern is specified in the box called regex.
        '''

        urls = get_urls.main(self.url.GetValue())
        pattern = re.compile(self.regex.GetValue())
        if urls:
            urls = '\n'.join(urls)

            filtered = re.findall(pattern,urls)
            filtered = '\n'.join(filtered)

            self.contents.SetValue(filtered)
    #--------------------------------------------------------------------------        
    def close(self,event):
        '''
        Destroys the window object.   
        '''
        self.win.Destroy()

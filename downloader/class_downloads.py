'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This is the preference class for open_pref function defined in class FlatMenu.
It creates the widgets like buttons and textAreas; packs them into container.
It also implements the binding of buttons to various events using functions to
browse location, save or cancel changes.

It imports:
    -wx
It defines:
    -__init__
    -clear_list
    -close
    -Populate
    -SetStringItem
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required Modules"""
import wx
import sys

from wx.lib.agw import aquabutton as AB
import  wx.lib.mixins.listctrl  as  listmix

import utils
from utils import opj

#---------------------------CONSTANTS---------------------------------------
tID = wx.NewId()

#--------------------------------------------------------------------------
class open_downloads(object):

    def __init__(self,win, panel):

        self.win = win
        self.panel = panel
        self.mainPanel = wx.Panel(panel)

        #window icon
        self.win.SetIcon(wx.Icon(opj('../Icons/Logo.png'),
                       wx.BITMAP_TYPE_PNG))
        
        #-------------------------------------------------------------------------------------------------------------
        #Creating widgets for window
        #-----------------------------------------------BUTTONS-------------------------------------------------------       
        clearbtn = AB.AquaButton(self.mainPanel, -1, None,
                                  "Clear List",size=(80,30))
        clearbtn.SetBackgroundColour((198,222,223,255))
        clearbtn.SetForegroundColour("Black")
        clearbtn.SetToolTipString("Click to clear list")
        clearbtn.Bind(wx.EVT_BUTTON, self.clear_list)

        closebtn = AB.AquaButton(self.mainPanel, -1, None,
                                  "Close",size=(80,30))
        closebtn.SetBackgroundColour((198,222,223,255))
        closebtn.SetForegroundColour("Black")
        closebtn.SetToolTipString("Close")
        closebtn.Bind(wx.EVT_BUTTON, self.close)

        #----------------------------------------------OTHER WIDGETS----------------------------------------------------
        #Downloads list
        #fetching downloads from content file
        with open(opj('../config/content.txt')) as content_file:
            data = content_file.read()

        download_point = data.find('DOWNLOADS')
        if download_point >= 0:
            end_point = data.find(']', download_point+1)
            DOWNLOADS = data[download_point+12:end_point+1]

        #Trailing extra whitespaces
        DOWNLOADS = utils.sanitize_string(DOWNLOADS)

        if DOWNLOADS != '[]':
            downloads = utils.string_to_tuple(DOWNLOADS)
        else:
            #setting empty tuple for downloads
            downloads = [('','')]

        self.downloads_list = {i+1:(entry[0],entry[1]) for i,entry in enumerate(downloads)}
        self.downloads_list_box = TestListCtrl(self.mainPanel, tID,
                                           (5,45),(472,240),
                                           style=wx.LC_REPORT
                                           | wx.BORDER_NONE
                                           | wx.LC_SORT_ASCENDING
                                           )
        
        self.Populate(self.downloads_list,self.downloads_list_box,"Time","URL")        

        #-------------------------------------------BUTTON-CONTAINER--------------------------------------------------
        button_cont = wx.BoxSizer()
        button_cont.Add(clearbtn,proportion=0,flag=wx.ALL)
        button_cont.Add(closebtn,proportion=0,flag=wx.LEFT,border=300)

        #-------------------------------------------WRAPPING BOXES----------------------------------------------------
        container = wx.StaticBox(self.mainPanel, -1)
        self.subSizer = wx.StaticBoxSizer(container,wx.VERTICAL)

        self.subSizer.Add(self.downloads_list_box,1,wx.EXPAND)

        #Wrraping the panel and its widgets
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.subSizer,1,wx.EXPAND|wx.ALL,border=0)
        panelSizer.Add(button_cont,0,wx.EXPAND)
        self.mainPanel.SetSizer(panelSizer)
        
        #wrap panel to window
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.mainPanel,1,wx.EXPAND)
        self.panel.SetSizer(self.mainSizer)
        
        self.panel.Layout()
        self.win.CenterOnScreen()
        self.win.Bind(wx.EVT_CLOSE,self.close)

    #-----------------------------------------------------------------------------------------------------------------
    def clear_list(self, event):
        '''
        clears downloads list
        '''
        DOWNLOADS = []
        self.downloads_list_box.DeleteAllItems()
        utils.write_downloads(DOWNLOADS,True)

    #-----------------------------------------------------------------------------------------------------------------
    def close(self, event):
        self.win.Destroy()

    #-----------------------------------------------------------------------------------------------------------------
    def Populate(self,list_,box,col1_head,col2_head):
        '''
        To create a downloads list
        '''
        # for normal, simple columns, you can add them like this:
        box.InsertColumn(0, col1_head)
        box.InsertColumn(1, col2_head)
        
        items = list_.items()
        for key, data in items:
            index = box.InsertStringItem(sys.maxint, data[0])
            box.SetStringItem(index, 0, data[0])
            box.SetStringItem(index, 1, data[1])
            box.SetItemData(index, key)

        box.SetColumnWidth(0, 150)
        box.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        box.currentItem = 0
        
    #-----------------------------------------------------------------------------------------------------------------
    def SetStringItem(self, index, col, data):
        '''
        Helper to create downloads list
        '''
        if col in range(2):
            wx.ListCtrl.SetStringItem(self, index, col, data)
            wx.ListCtrl.SetStringItem(self, index, 2+col, str(len(data)))
        else:
            try:
                datalen = int(data)
            except:
                return

            wx.ListCtrl.SetStringItem(self, index, col, data)

            data = self.GetItem(index, col-2).GetText()
            wx.ListCtrl.SetStringItem(self, index, col-2, data[0:datalen])
            
    #-----------------------------------------------------------------------------------------------------------------
    
class TestListCtrl(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin):#,
#                   listmix.TextEditMixin):
    '''
    Class for implementing List Ctrl for downloads 
    '''

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        listmix.ListCtrlAutoWidthMixin.__init__(self)
#        listmix.TextEditMixin.__init__(self)

    #-------------------------------------------------------------------
    def OnItemSelected(self, event):
        #so that it refers to the global constant
        global filters
        #index of the selected item
        cur_item = event.m_itemIndex
        #the item
        item = self.GetItem(cur_item, 1)
        filters = item.GetText()  

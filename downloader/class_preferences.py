'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This script is used by Menu class to implement preferences window using
the OpenPref class defined here.

It imports:
    -wx
    -sys
    -listmix from wx.lib.mixins.listctrl
    -opj from utils
    -utils
It defines:
  -OpenPref
    -__init__
    -Create_Toolbar
    -General
    -Filters
    -History
    -Populate
    -SetStringItem
    -Browse
    -Save
    -close
  -TestListCtrl
    -__init__
    -OnItemSelected
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required Modules"""
import wx
import sys

import  wx.lib.mixins.listctrl  as  listmix

from utils import opj
import utils

#---------------------------CONSTANTS-----------------------------------------
#flags for toolbar
TBFLAGS = ( wx.TB_HORIZONTAL
            | wx.NO_BORDER
            | wx.TB_FLAT
            | wx.TB_TEXT
            | wx.TB_HORZ_LAYOUT
            )
tID = wx.NewId()
#id's for toolbar tools
GENERAL_ID = wx.NewId()
FILTER_ID = wx.NewId()
HISTORY_ID = wx.NewId()
DOWNLOAD_ID = wx.NewId()

#options for history configuration
HISTORY_OPTIONS = ['Always save history','Never save history']
#renaming options
CHOICE_LIST = ['Rename', 'Replace', 'Cancel']
#segment options
SEGMENT_OPTIONS = ['Default','2', '4', '8']

DD=''; FILTERS=''; OPTION_SELECTED=''; RADIO_SELECTED=''; SEGMENT_SELECTED='';

#--------------------fetching configurations from config file-----------------
def read_config():
    '''
    Function to read configurations from config file.
    '''
    global DD, FILTERS, OPTION_SELECTED, RADIO_SELECTED, SEGMENT_SELECTED
    with open(opj('config/config.txt')) as config_file:
        data = config_file.read()

    #default_dir
    dir_point = data.find('PATH')
    if dir_point >= 0:
        end_point = data.find('\n',dir_point+1)
        DD = data[dir_point+7:end_point]

    #filter
    filter_point = data.find('FILTER')
    if filter_point >= 0:
        end_point = data.find('\n',filter_point+1)
        FILTERS = data[filter_point+9:end_point]

    #history_option
    opt_point = data.find('OPTION')
    if opt_point >= 0:
        end_point = data.find('\n',opt_point+1)
        OPTION_SELECTED = data[opt_point+9:end_point]

    #rename option
    radio_point = data.find('RENAME')
    if radio_point >= 0:
        end_point = data.find('\n',radio_point+1)
        RADIO_SELECTED = data[radio_point+9:end_point].strip()

    #segment option
    segment_point = data.find('SEGMENT')
    if segment_point >= 0:
    	end_point = data.find('\n', segment_point+1)
    	SEGMENT_SELECTED = data[segment_point+10:end_point].strip()

    #Trailing extra whitespaces
    var = [DD, FILTERS, OPTION_SELECTED, RADIO_SELECTED, SEGMENT_SELECTED]
    DD, FILTERS, OPTION_SELECTED, RADIO_SELECTED, SEGMENT_SELECTED = utils.sanitize_string(var)

#---------------------------------------------------------------------------------------------------------------------
class OpenPref(object):
    '''
    This is the preference class for open_pref function defined in class Menu.
    It creates the widgets like buttons and textAreas; packs them into container.
    It also implements the binding of buttons to various events using functions to
    browse location, save or cancel changes.
    '''

    def __init__(self,win, panel):
        #selected option for history to show on first appearence of window
        global OPTION_SELECTED, RADIO_SELECTED, SEGMENT_SELECTED

        self.win = win
        self.panel = panel
        self.mainPanel = wx.Panel(panel)
        self.win.MakeModal()

        #window icon
        self.win.SetIcon(wx.Icon(opj('Icons/Logo.png'),
                       wx.BITMAP_TYPE_PNG))

        #reading configurations
        read_config()
        
        #-------------------------------------------------------------------------------------------------------------
        #                                   Creating widgets for window
        #-----------------------------------------------BUTTONS-------------------------------------------------------
        OKbtn = wx.Button(self.mainPanel, -1,
                                "OK",size=(60,25))
        OKbtn.SetForegroundColour("Black")
        OKbtn.SetToolTipString("Save changes")
        OKbtn.Bind(wx.EVT_BUTTON, self.Save)
        
        cancelbtn = wx.Button(self.mainPanel, -1,
                                  "Cancel",size=(60,25))
        cancelbtn.SetForegroundColour("Black")
        cancelbtn.SetToolTipString("Click to cancel changes")
        cancelbtn.Bind(wx.EVT_BUTTON, self.Cancel)

        browse_btn = wx.BitmapButton(self.mainPanel, -1, wx.Bitmap(opj('Icons/folder.png')),
                                     size=(32,25))
        browse_btn.SetBackgroundColour((198,222,223,255))
        browse_btn.SetForegroundColour("Black")
        browse_btn.SetToolTipString("Select location")
        browse_btn.Bind(wx.EVT_BUTTON,self.Browse)

        clearbtn = wx.Button(self.mainPanel, -1,
                                            "Clear History",size=(80,25))
        clearbtn.SetForegroundColour("Black")
        clearbtn.SetToolTipString("Click to clear list")
        clearbtn.Bind(wx.EVT_BUTTON, self.Clear_List)
        
        #----------------------------------------------OTHER WIDGETS----------------------------------------------------
        #-------------------Text ctrl for showing selected location----------------------------
        self.dir = wx.TextCtrl(self.mainPanel,size=(400,25),
                               style=wx.TE_READONLY)
        self.dir.SetValue(DD)
        self.dir.Disable()
        self.dir.SetToolTipString("Selected default location");

        #----------------------combobox for saving history-------------------------------------
        history_label = wx.StaticText(self.mainPanel,-1,"Downloader will:",
                                       size=(90,15))
        self.history = wx.ComboBox(self.mainPanel, -1,OPTION_SELECTED,
                                   choices=HISTORY_OPTIONS,style=wx.CB_DROPDOWN
                                   |wx.CB_READONLY)

        #-----------------------radio box for renaming options---------------------------------
        rename = wx.RadioButton(self.mainPanel, -1, CHOICE_LIST[0], style = wx.RB_GROUP )
        replace = wx.RadioButton(self.mainPanel, -1, CHOICE_LIST[1] )
        cancel = wx.RadioButton(self.mainPanel, -1, CHOICE_LIST[2] )
        self.radio_list = [rename, replace, cancel]
		
        #setting radio selected for previous choice
        if RADIO_SELECTED:
            index = CHOICE_LIST.index(RADIO_SELECTED)
        else: index = 0
        self.radio_list[index].SetValue(1)

		#-----------------------segment box for segmentation options---------------------------
        default = wx.RadioButton(self.mainPanel, -1, SEGMENT_OPTIONS[0], style = wx.RB_GROUP )
        two = wx.RadioButton(self.mainPanel, -1, SEGMENT_OPTIONS[1])
        four = wx.RadioButton(self.mainPanel, -1, SEGMENT_OPTIONS[2] )
        eight = wx.RadioButton(self.mainPanel, -1, SEGMENT_OPTIONS[3] )
        self.segment_list = [default,two, four, eight]

        #setting radio selected for previous choice
        if SEGMENT_SELECTED:
            index = SEGMENT_OPTIONS.index(SEGMENT_SELECTED)
        else: index = 0
        self.segment_list[index].SetValue(1)

        #-----------------------------------Filters list----------------------------------------
        self.filter_list = {1:('Images(jpg,jpeg,gif,...)',
                                '.*\.(?:jp(?:e?g|e|2)|gif|png|tiff?|bmp|ico)$'),
                            2:('Archives(zip,rar,...)',
                                '.*\.(?:z(?:ip|[0-9]{2})|r(?:ar|[0-9]{2})|jar|bz2|gz|tar|rpm|7z(?:ip)?|lzma|xz)$'),
                            3:('Audio(mp3,wav,...)',
                                '.*\.(?:mp3|wav|og(?:g|a)|flac|midi?|rm|aac|wma|mka|ape)$'),
                            4:('Software(exe,xpi,...)',
                                '.*\.(?:exe|msi|dmg|bin|xpi|iso)$'),
                            5:('Videos(mpeg,avi,...)',
                                '.*\.(?:mpeg|ra?m|avi|mp(?:g|e|4)|mov|divx|asf|qt|wmv|m\dv|rv|vob|asx|ogm|ogv|webm)$'),
                            6:('Documents(pdf,odf,...)',
                                '.*\.(?:pdf|xlsx?|docx?|odf|odt|rtf)$')
                            }
        self.filter_list_box = TestListCtrl(self.mainPanel, tID,
                                           (5,45),(472,240),
                                           style=wx.LC_REPORT
                                           | wx.BORDER_NONE
                                           | wx.LC_SORT_ASCENDING
                                           )
        
        self.Populate(self.filter_list,self.filter_list_box,"Caption","Extension")
        self.win.Bind(wx.EVT_LIST_ITEM_SELECTED,
                      self.filter_list_box.OnItemSelected,
                      self.filter_list_box)
        
        #-----------------------------------History list------------------------------------------
        #fetching downloads from content file
        with open(opj('config/content.txt')) as content_file:
            data = content_file.read()
            
        history_point = data.find('HISTORY')
        if history_point >= 0:
            end_point = data.find(']', history_point+1)
            HISTORY = data[history_point+10:end_point+1]

            #Trailing extra whitespaces
            HISTORY = utils.sanitize_string(HISTORY)
            #converting the string of history to tuple.
            history = utils.string_to_tuple(HISTORY)
        else:
            HISTORY = '[]'
            history = [('','')]

        self.history_list = {i+1:(entry[0],entry[1]) for i,entry in enumerate(history)}

        self.history_list_box = TestListCtrl(self.mainPanel, tID,
                                           (5,45),(472,240),
                                           style=wx.LC_REPORT
                                           | wx.BORDER_NONE
                                           | wx.LC_SORT_ASCENDING
                                           )
        
        self.Populate(self.history_list,self.history_list_box,"URL","Time")        

        #-------------------------------------------------CONTAINERS--------------------------------------------------
        #---------------------------------for directory box---------------------------------------
        dir_box = wx.BoxSizer()
        dir_box.Add(self.dir,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        dir_box.Add(browse_btn,proportion=0,border=5,flag=wx.ALL)

        #----------------------------------for history box----------------------------------------
        history_btn_cont = wx.BoxSizer()
        history_btn_cont.Add(clearbtn,proportion=0,border=370,flag=wx.LEFT)
        
        history_widgets = wx.BoxSizer()
        history_widgets.Add(history_label,proportion=0,flag=wx.ALL|wx.EXPAND,border=10)
        history_widgets.Add(self.history,proportion=1,border=5,flag=wx.ALL)
        
        history_box = wx.BoxSizer(wx.VERTICAL)
        history_box.Add(history_widgets,1,wx.EXPAND)
        history_box.Add(history_btn_cont)

        #-----------------------------------for rename radio buttons-----------------------------
        rename_box = wx.FlexGridSizer(cols=3,hgap=80)
        rename_box.AddMany((rename,replace,cancel))

        #-----------------------------------for segment radio buttons----------------------------
        segment_box = wx.FlexGridSizer(cols=4,hgap=60)
        segment_box.AddMany((default,two,four,eight))

        #----------------------------------Static box for dir_container--------------------------
        box = wx.StaticBox(self.mainPanel,-1,"Choose default directory",
                           size=(500,25))
        self.dir_sizer = wx.StaticBoxSizer(box)
        self.dir_sizer.Add(dir_box,1,wx.EXPAND)

        #--------------------------------static box for history container------------------------
        box = wx.StaticBox(self.mainPanel,-1,"History preferences",
                           size=(500,25))
        self.history_sizer = wx.StaticBoxSizer(box)
        self.history_sizer.Add(history_box,1,wx.EXPAND)

        #---------------------------------static box for rename container------------------------
        box = wx.StaticBox(self.mainPanel,-1,"If a file already exist",
                           size=(500,25))
        self.rename_sizer = wx.StaticBoxSizer(box)
        self.rename_sizer.Add(rename_box,1,wx.EXPAND|wx.ALL,border=5)

        #--------------------------------static box for segment container------------------------
        box = wx.StaticBox(self.mainPanel,-1,"Choose no. of segments for download",
                           size=(500,25))
        self.segment_sizer = wx.StaticBoxSizer(box)
        self.segment_sizer.Add(segment_box,1,wx.EXPAND|wx.ALL,border=5)

        #--------------------------------Button container----------------------------------------
        button_cont = wx.BoxSizer()
        button_cont.Add(cancelbtn,proportion=0,flag=wx.ALL,border=5)
        button_cont.Add(OKbtn,proportion=0,flag=wx.ALL,border=5)

        #-------------------------------------------WRAPPING BOXES----------------------------------------------------
        container = wx.StaticBox(self.mainPanel, -1)
        self.subSizer = wx.StaticBoxSizer(container,wx.VERTICAL)

        self.subSizer.Add(self.dir_sizer,0,wx.EXPAND|wx.TOP, border=5)
        self.subSizer.Add(self.filter_list_box,1,wx.EXPAND)
        self.subSizer.Add(self.history_list_box,1,wx.EXPAND)
        self.subSizer.Add(self.history_sizer,0,wx.EXPAND|wx.TOP, border=5)
        self.subSizer.Add(self.rename_sizer,0,wx.EXPAND|wx.TOP, border=5)
        self.subSizer.Add(self.segment_sizer,0,wx.EXPAND|wx.TOP, border=5)

        #--------------Wrraping the panel and its widgets----------------------------------------
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.subSizer,1,wx.EXPAND|wx.ALL,border=5)
        panelSizer.Add(button_cont,0,wx.EXPAND)
        self.mainPanel.SetSizer(panelSizer)
        
        self.Create_Toolbar(win)

        #--------------Wrap menu and panel to window---------------------------------------------
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.toolBar,0,wx.EXPAND)
        self.mainSizer.Add(self.mainPanel,1,wx.EXPAND)
        self.panel.SetSizer(self.mainSizer)
        
        self.panel.Layout()
        self.General()
        self.win.CenterOnScreen()
        self.win.Bind(wx.EVT_CLOSE,self.Cancel)

    #-----------------------------------------------------------------------------------------------------------------
    def Create_Toolbar(self,win):
        '''
        Method to create toolbar.
        '''
        self.toolBar = wx.ToolBar(self.panel, style=TBFLAGS)
        tsize = (30,30)
                
        #---------------------------------------Toolbar icons------------------------------------
        general_bmp = wx.Bitmap(opj("Icons/pref.png"), wx.BITMAP_TYPE_PNG)
        filter_bmp = wx.Bitmap(opj("Icons/new.png"), wx.BITMAP_TYPE_PNG)
        history_bmp = wx.Bitmap(opj("Icons/package.png"), wx.BITMAP_TYPE_PNG)
        history_bmp = wx.Bitmap(opj("Icons/package.png"), wx.BITMAP_TYPE_PNG)

        #---------------------------------------Tools--------------------------------------------
        self.toolBar.SetToolBitmapSize(tsize)
        self.toolBar.AddLabelTool(GENERAL_ID, "&General", general_bmp, shortHelp="General")
        self.win.Bind(wx.EVT_TOOL, self.General, id=GENERAL_ID)

        self.toolBar.AddLabelTool(FILTER_ID, "&Filters", filter_bmp, shortHelp="Filters")
        self.win.Bind(wx.EVT_TOOL, self.Filters, id=FILTER_ID)

        self.toolBar.AddLabelTool(HISTORY_ID, "&History", history_bmp, shortHelp="History")
        self.win.Bind(wx.EVT_TOOL, self.History, id=HISTORY_ID)

        self.toolBar.AddLabelTool(DOWNLOAD_ID, "&Downloads", history_bmp, shortHelp="Downloads")
        self.win.Bind(wx.EVT_TOOL, self.Downloads, id=DOWNLOAD_ID)

        #-----------------------------------------------------------------------------------------
        self.toolBar.Realize()    

    #-----------------------------------------------------------------------------------------------------------------
    def General(self, *event):
        '''
        Method called when General tool clicked.
        '''
        try:
            #-----------------------------hide all other widgets.--------------------------------
            self.subSizer.Hide(self.dir_sizer)
            self.subSizer.Hide(self.history_sizer)
            self.subSizer.Hide(self.rename_sizer)
            self.subSizer.Hide(self.segment_sizer)
            self.subSizer.Hide(self.filter_list_box)
            self.subSizer.Hide(self.history_list_box)
        except Exception as e:
            print e

        #---------------------------------show general tool's widgets----------------------------
        self.subSizer.Show(self.dir_sizer)
        self.subSizer.Show(self.rename_sizer)
        self.subSizer.Show(self.history_sizer)
        self.panel.Layout()
        
    #-----------------------------------------------------------------------------------------------------------------
    def Filters(self, event):
        '''
        Method called when Filters tool clicked.
        '''
        try:
            #-----------------------------hide all other widgets.--------------------------------
            self.subSizer.Hide(self.dir_sizer)
            self.subSizer.Hide(self.history_sizer)
            self.subSizer.Hide(self.rename_sizer)
            self.subSizer.Hide(self.filter_list_box)
            self.subSizer.Hide(self.history_list_box)
        except Exception as e:
            print e
        
        #---------------------------------show filter tool's widgets----------------------------
        self.subSizer.Show(self.filter_list_box)
        
        self.panel.Layout()
        
    #-----------------------------------------------------------------------------------------------------------------
    def History(self, event):
        '''
        Method called when History tool clicked.
        '''
        try:
            #-----------------------------hide all other widgets.--------------------------------
            self.subSizer.Hide(self.dir_sizer)
            self.subSizer.Hide(self.history_sizer)
            self.subSizer.Hide(self.rename_sizer)
            self.subSizer.Hide(self.filter_list_box)
            self.subSizer.Hide(self.history_list_box)
        except Exception as e:
            print e

        #---------------------------------show history tool's widgets----------------------------            
        self.subSizer.Show(self.history_list_box)
        
        self.panel.Layout()

    #-----------------------------------------------------------------------------------------------------------------
    def Downloads(self, event):
        try:
            #-----------------------------hide all other widgets.--------------------------------
            self.subSizer.Hide(self.dir_sizer)
            self.subSizer.Hide(self.history_sizer)
            self.subSizer.Hide(self.rename_sizer)
            self.subSizer.Hide(self.segment_sizer)
            self.subSizer.Hide(self.filter_list_box)
            self.subSizer.Hide(self.history_list_box)
        except Exception as e:
            print e

        #---------------------------------show download tool's widgets----------------------------                        
        self.subSizer.Show(self.segment_sizer)
        
        self.panel.Layout()

    #-----------------------------------------------------------------------------------------------------------------
    def Populate(self,list_,box,col1_head,col2_head):
        '''
        Helper to Filters, and History method.
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

        box.SetColumnWidth(0, 300)
        box.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        box.currentItem = 0
        
    #-----------------------------------------------------------------------------------------------------------------
    def SetStringItem(self, index, col, data):
        '''
        Helper to Filters, and History method.
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
    def Browse(self, event):
        '''
        The function is bind with the browse button.
        It opens a directory location, and set it as default
        '''
        global DD
        dir_= self.dir.GetValue()
        dlg = wx.DirDialog(self.win, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
                           | wx.DD_CHANGE_DIR
                           )

        dlg.SetPath(dir_)
        if dlg.ShowModal() == wx.ID_OK:
            DD = dlg.GetPath()
            self.dir.SetValue(DD)

        dlg.Destroy()

    #-----------------------------------------------------------------------------------------------------------------
    def Save(self, event):
        '''
        The function is bind with the save button.
        It saves all the changes in preferences.
        '''
        global OPTION_SELECTED,  RADIO_SELECTED

        #index of selection
        select_index = self.history.GetSelection()
        #selected option string
        OPTION_SELECTED = HISTORY_OPTIONS[select_index]
        #radio selection
        select_index = [self.radio_list.index(x) for x in self.radio_list if x.GetValue()][0]
        RADIO_SELECTED = CHOICE_LIST[select_index]
        #segment selection
        select_index = [self.segment_list.index(x) for x in self.segment_list if x.GetValue()][0]
        SEGMENT_SELECTED = SEGMENT_OPTIONS[select_index]
        #changing configuration
        utils.change_config(DD,FILTERS,OPTION_SELECTED,RADIO_SELECTED,SEGMENT_SELECTED)
        self.win.MakeModal(False)
        self.win.Destroy()
    #-----------------------------------------------------------------------------------------------------------------
    def Cancel(self, event):
        '''
        The method is bound with the save button.
        It saves all the changes in preferences.
        '''
        self.win.MakeModal(False)
        self.win.Destroy()

    #-----------------------------------------------------------------------------------------------------------------
    def Clear_List(self, event):
        '''
        The method to clear history list.
        '''
        self.history_list_box.DeleteAllItems()

        #true is an argument to tell the function to clear all history.
        utils.write_history('',True)

    #-----------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------
class TestListCtrl(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin):#,
#                   listmix.TextEditMixin):
    '''
    Class for implementing List Ctrl for Filters, and history.
    '''

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        listmix.ListCtrlAutoWidthMixin.__init__(self)
#        listmix.TextEditMixin.__init__(self)

    #-------------------------------------------------------------------
    def OnItemSelected(self, event):
        #so that it refers to the global constant
        global FILTERS
        #index of the selected item
        cur_item = event.m_itemIndex
        #the item
        item = self.GetItem(cur_item, 1)
        FILTERS = item.GetText()  

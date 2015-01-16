'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This script is used by the entry script SJdownloader to create a window panel
and its widgets using the Mypanel class defined here.

It imports:
    -wx
    -re
    -json
    -platform
    -aquabutton from wx.lib.agw
    -pygauge from wx.lib.agw
    -get_urls
    -downloader_script
    -Menu from class_Menu
    -utils
    -opj form utils
    -class_preferences
It defines:
  -Mypanel
    -__init__
    -Evt_Check_Box
    -Select_All
    -Select_Default
    -Enter
    -Filter
    -Download
    -Browse
    -Reset
    -Cancel
    -Close
    -Enable_Checkes
    -Evt_Check_List_Box
    -Make_Pattern
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""Required modules"""
import re
import wx
import json
import platform
from wx.lib.agw import aquabutton as AB
from wx.lib.agw import pygauge as PG

import get_urls
import downloader_script
from class_Menu import Menu
import utils
from utils import opj
import class_preferences

#---------------------------Global constants---------------------------------
DEFAULT_DIR='.'
FILTERS=''

#----------------reading configurations from config file---------------------
def read_config():
    '''
    Function to read configuration options from config file.
    '''
    global DEFAULT_DIR, FILTERS
    try:
        config_file = open(opj('config/config.json'))
        data = json.load(config_file)
        config_file.close()

        #default_dir
        DEFAULT_DIR = data["configuration"]["PATH"]
        if DEFAULT_DIR == "":
            DEFAULT_DIR = '.'

        #filter
        FILTERS = data["configuration"]["FILTER"]

    except ValueError:
        pass

    #trailing extra whitespaces
    DEFAULT_DIR, FILTERS = utils.sanitize_string([DEFAULT_DIR, FILTERS])

#--------------------------------------------------------------------------------------------
class Mypanel(object):
    '''
    This is the Mypanel class for GUI module.
    It creates the widgets like buttons and textAreas, checkboxes; packs them into container.
    It also implements the binding of buttons to various events using functions to
    filter, browse location, and download content.
    '''
    def __init__(self,panel,win):
        self.win = win                                              #The window object
        self.panel = panel                                          #The panel object
        self.panel.SetBackgroundColour((198,222,223,255))
        self.panel.SetForegroundColour((60,60,60,255))
        
        #window icon
        self.win.SetIcon(wx.Icon(opj('Icons/sjdownloader-logo.png'),
                       wx.BITMAP_TYPE_PNG))

        #reading configurations
        read_config()
                       
        #upper container for logo, description, url and dir
        box = wx.StaticBox(self.panel, -1,size=(500,50))
        self.introsizer = wx.StaticBoxSizer(box,wx.VERTICAL)

        #---------------------------------Images---------------------------------------------
        #LOGO
        png = wx.Image(opj('Icons/sjdownloader-logo.png'),
                       wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        logo = wx.StaticBitmap(panel, -1, png)
        
        #folder
        png = wx.Image(opj('Icons/folder.png'),
                       wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        folder_icon = wx.StaticBitmap(panel, -1, png,size=(25,22))

        #------------------------------Description-------------------------------------------      
        sub_container_one = wx.BoxSizer()
        sub_container_two = wx.BoxSizer(wx.VERTICAL)

        #--------------------------------Linux-------------------------------------------
        if platform.system() == "Linux":

            description = wx.TextCtrl(self.panel, -1,"SJdownloader\n",size=(470,72),
                                      style=wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_NO_VSCROLL|
                                      wx.TE_READONLY|wx.ALIGN_CENTER)
            font = wx.Font(20, wx.SWISS,wx.NORMAL, wx.BOLD, False, "Courier New")
            description.SetStyle(0,12,wx.TextAttr("WHITE",(0,162,232,255),font))
            description.AppendText("A free internet downloader, Now download It all, just enter the url and click start! For more click Show Links!")
            font = wx.Font(9, wx.SWISS,wx.NORMAL, wx.BOLD, False, "Courier New")
            description.SetStyle(13,-1,wx.TextAttr("BLACK",(0,162,232,255),font))

        #--------------------------------Windows-----------------------------------------
        elif platform.system() == "Windows":

            description = wx.TextCtrl(self.panel, -1,"\t\t\tSJdownloader\n",size=(460,72),
                                      style=wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_NO_VSCROLL|
                                      wx.TE_READONLY)
            font = wx.Font(20, wx.SWISS,wx.NORMAL, wx.BOLD, False, "Courier New")
            description.SetStyle(0,15,wx.TextAttr("WHITE",(0,162,232,255),font))
            description.AppendText("A free internet downloader, Now download It all,\
    just enter the url and click start! For more click Show Links!")
            font = wx.Font(9, wx.SWISS,wx.NORMAL, wx.BOLD, False, "Courier New")
            description.SetStyle(17,126,wx.TextAttr("BLACK",(0,162,232,255),font))

        #--------------------------------------------------------------------------------
        description.SetBackgroundColour((0,162,232,255))
        sub_container_one.Add(logo)
        sub_container_one.Add(description)
        
        sub_container_one.Layout()
        
        # self.introsizer.Add(logo,proportion=0)
        self.introsizer.Add(sub_container_one,proportion=1,flag=wx.EXPAND)
        self.introsizer.Add(sub_container_two,proportion=0,flag=wx.EXPAND)

        #--------------------------Buttons and events----------------------------------------      
        #calls (Enter) method
        show_btn = AB.AquaButton(panel, -1, None, "Links",size=(70,22))
        show_btn.SetBackgroundColour((98,208,255,255))
        show_btn.SetForegroundColour("Black")
        show_btn.SetToolTipString("Click to show found links")
        show_btn.Bind(wx.EVT_BUTTON,self.Enter)

        #calls Browse method;
        browse_btn = AB.AquaButton(panel, -1, None, "Browse",size=(70,22))
        browse_btn.SetBackgroundColour((98,208,255,255))
        browse_btn.SetForegroundColour("Black")
        browse_btn.SetToolTipString("Select location")
        browse_btn.Bind(wx.EVT_BUTTON,self.Browse)
        
        #calls Reset method
        reset_btn = AB.AquaButton(panel, -1, None, "Reset",size=(70,25))
        reset_btn.SetBackgroundColour((98,208,255,255))
        reset_btn.SetForegroundColour("Black")
        reset_btn.SetToolTipString("Reset downloader")
        reset_btn.Bind(wx.EVT_BUTTON,self.Reset)

        #calls Download metod
        self.download_btn = AB.AquaButton(panel, -1, None, "Start",size=(70,25))
        self.download_btn.SetBackgroundColour((98,208,255,255))
        self.download_btn.SetForegroundColour("Black")
        self.download_btn.SetToolTipString("Start download")
        self.download_btn.Bind(wx.EVT_BUTTON,self.Download)

        #calls Close method        
        close_btn = AB.AquaButton(panel, -1, None, "Close",size=(70,25))
        close_btn.SetBackgroundColour((98,208,255,255))
        close_btn.SetForegroundColour("Black")
        close_btn.SetToolTipString("Close")
        close_btn.Bind(wx.EVT_BUTTON,self.Close)

        #calls cancle method        
        self.cancel_btn = AB.AquaButton(panel, -1, None, "Cancel",size=(70,25))
        self.cancel_btn.SetBackgroundColour((98,208,255,255))
        self.cancel_btn.SetForegroundColour("Black")
        self.cancel_btn.SetToolTipString("Cancel download")
        self.cancel_btn.Bind(wx.EVT_BUTTON,self.Cancel)
        self.cancel_btn.Disable()

        #calls filter method
        self.filter_btn = AB.AquaButton(panel, -1, None, "Filter",size=(70,25))
        self.filter_btn.SetBackgroundColour((98,208,255,255))
        self.filter_btn.SetForegroundColour("Black")
        self.filter_btn.SetToolTipString("Filter links")
        self.filter_btn.Bind(wx.EVT_BUTTON,self.Filter)
        self.filter_btn.Disable()
        
        #--------------------------TEXT AREAS------------------------------------------------
        #Static text area:

        #Label, before text box for url
        url = wx.StaticText(panel, -1, "URL:",size=(70,15))
     
        #Label, before text box for dir location
        location = wx.StaticText(panel, -1, "Save file in:",size=(70,15))
        #Count of links
        self.count = wx.StaticText(self.panel,-1,"No. of links found:",
                                       size=(255,15),pos=(420,295))
        #Label, before regex text box
        regex = wx.StaticText(panel, -1, "Enter regex:",pos=(400,310))
        #progress label
        progress = wx.StaticText(panel, -1, "Progress")

        #--------------------------------------------------------------------------
        
        #-----------------------------text box for url-----------------------------
        self.url_field = wx.TextCtrl(panel,
                                     size=(0,10),pos=(5,5),                                     
                                     style=wx.TE_PROCESS_ENTER,
                                     )
        self.url_field.SetToolTipString("Enter url here");
        self.url_field.SetFocus()                                                                   
        
        #---------------------text box for showing dir location--------------------
        self.dir = wx.TextCtrl(panel,size=(0,10),pos=(5,30))
        #set directory value
        self.dir.SetValue(DEFAULT_DIR)

        self.dir.SetToolTipString("Selected location to save file");

        #--------------------Static box For showing links--------------------------
        self.box = wx.StaticBox(self.panel, -1, "The links will be shown here")
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        
        #-----------------text box for entering regex pattern----------------------
        self.regex = wx.TextCtrl(panel,size=(200,25))
        self.regex.SetToolTipString("Enter type string to filter content");
        self.regex.SetEditable(False)

        #----------------------------Progress bar----------------------------------
        self.progress = PG.PyGauge(panel,-1,size=(255,20),style=wx.GA_HORIZONTAL)

        #-------------------------------CHECKBOXES-------------------------------------------
        self.cb1 = wx.CheckBox(panel, -1, "jpeg",
                          (5, 295), (75, 20))
        self.cb2 = wx.CheckBox(panel, -1, "png",
                          (5, 310), (75, 20))
        self.cb3 = wx.CheckBox(panel, -1, "gif",
                          (5, 335), (75, 20))
        self.cb4 = wx.CheckBox(panel, -1, "mp4",
                          (35, 295), (75, 20))
        self.cb5 = wx.CheckBox(panel, -1, "3gp",
                          (35,310), (75, 20))
        self.cb6 = wx.CheckBox(panel, -1, "avi",
                          (35, 335), (75, 20))
        self.cb7 = wx.CheckBox(panel, -1, "flv",
                          (70, 295), (55, 20))
        self.cb8 = wx.CheckBox(panel, -1, "mp3",
                          (70, 310), (55, 20))
        self.cb9 = wx.CheckBox(panel, -1, "jpg",
                          (70, 310), (55, 20))
        self.select_all = wx.CheckBox(self.panel, -1, "select all",
                              (70, 310), (85, 15))
        self.select_default = wx.CheckBox(self.panel, -1, "Apply default filter",
                              (70, 310), (400, 20))
        self.select_default.Enable(False)
        self.Enable_Checkes(False)

        #--------------------Binding events with checkboxes---------------------
        self.cb1.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb2.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb3.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb4.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb5.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb6.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb7.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb8.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.cb9.Bind(wx.EVT_CHECKBOX, self.Evt_Check_Box)
        self.select_all.Bind(wx.EVT_CHECKBOX, self.Select_All)
        self.select_default.Bind(wx.EVT_CHECKBOX, self.Select_Default)
        
        #----------------------------WRAPPING UP THE BOXES-----------------------------------
        #The text controls
        #-----------------

        #The url, url label containers                           Container#1 
        url_box = wx.BoxSizer()                                  
        url_box.Add(url,proportion=0,flag=wx.TOP|wx.RIGHT,border=7)
        url_box.Add(self.url_field,proportion=1,flag=wx.EXPAND|
                    wx.ALL,border=2)
        url_box.Add(show_btn,proportion=0,border=5,flag=wx.LEFT|wx.TOP)

        #The dir location, location label container              Container#2 
        dir_box = wx.BoxSizer()
        dir_box.Add(location,proportion=0,flag=wx.TOP|wx.RIGHT,border=5)
        dir_box.Add(self.dir,proportion=1,flag=wx.ALL|wx.EXPAND,border=2)
        dir_box.Add(folder_icon,proportion=0,border=5,flag=wx.TOP)#|wx.RIGHT)
        dir_box.Add(browse_btn,proportion=0,border=5,flag=wx.LEFT|wx.TOP)
        #--------------------------------------------------------------------------
        #For select all and count box
        self.hbox = wx.FlexGridSizer(cols=2,hgap=250)
        self.hbox.Add(self.select_all,proportion=0,flag=wx.LEFT|
                      wx.RIGHT,border=3)
        self.hbox.Add(self.count,proportion=1,flag=wx.LEFT|
                      wx.RIGHT,border=3)
        
        #container for main output box                           Container#3
        Static_box = wx.BoxSizer()
        Static_box.Add(self.bsizer,proportion=1,flag=wx.EXPAND
                  |wx.LEFT|wx.RIGHT|wx.BOTTOM,border=5
                  )
        Static_box.Add(reset_btn,proportion=0,border=5,flag=wx.LEFT|wx.TOP)
        #--------------------------------------------------------------------------
        
        #--------------
        #The checkBoxes
        #--------------
        #First set of boxes vertically
        feature_box1 = wx.BoxSizer(wx.VERTICAL)
        
        feature_box1.Add(self.cb1, proportion=0,flag=wx.EXPAND     #jpeg
                      |wx.LEFT,border=5)
        feature_box1.Add(self.cb2, proportion=0,flag=wx.EXPAND     #png
                      |wx.LEFT,border=5)
        feature_box1.Add(self.cb3, proportion=0,flag=wx.EXPAND     #gif
                      |wx.LEFT,border=5)

        #Second set of boxes vertically
        feature_box2 = wx.BoxSizer(wx.VERTICAL)
        feature_box2.Add(self.cb4, proportion=0,flag=wx.EXPAND     #mp4
                      |wx.ALL)
        feature_box2.Add(self.cb5, proportion=0,flag=wx.EXPAND     #3gp
                      |wx.ALL)
        feature_box2.Add(self.cb6, proportion=0,flag=wx.EXPAND     #avi
                      |wx.ALL)

        #Third set of boxes vertically
        feature_box3 = wx.BoxSizer(wx.VERTICAL)
        feature_box3.Add(self.cb7, proportion=0,flag=wx.EXPAND     #flv
                      |wx.ALL)
        feature_box3.Add(self.cb8, proportion=0,flag=wx.EXPAND     #mp3
                      |wx.ALL)
        feature_box3.Add(self.cb9, proportion=0,flag=wx.EXPAND     #jpg
                      |wx.ALL)
        #--------------------------------------------------------------------------
        
        #-------------------
        #Extra feature boxes
        #-------------------
        #container for regex text box and filter button
        regex_box = wx.FlexGridSizer(cols=3, vgap=10, hgap=3)
        regex_box.Add(regex,proportion=0,flag=wx.TOP,border=7)
        regex_box.Add(self.regex,proportion=1,flag=wx.BOTTOM|wx.LEFT
                      |wx.EXPAND|wx.RIGHT,border=5)
        regex_box.Add(self.filter_btn,proportion=0,
                      flag=wx.TOP|wx.RIGHT|wx.BOTTOM,border=3)

        #container for (regex,Filter) container and count text box
        feature_box4 = wx.BoxSizer(wx.VERTICAL)
        feature_box4.Add(regex_box,proportion=0,flag=wx.ALL)
        feature_box4.Add(self.select_default,proportion=1,flag=wx.TOP,border=2)
        
        #--------------------------------------------------------------------------
        #container for (checkbox, extra feature) containers     Container#4
        feature_box = wx.BoxSizer()
        feature_box.Add(feature_box1,proportion=0)
        feature_box.Add(feature_box2,proportion=0)
        feature_box.Add(feature_box3,proportion=0)
        feature_box.Add(feature_box4,proportion=0,flag=wx.EXPAND)

        #--------------------------------------------------------------------------
        
        #container for progres bar                              Container#5
        prog_box = wx.BoxSizer()
        prog_box.Add(progress, proportion=0, flag=wx.ALL,border=5)
        prog_box.Add(self.progress,proportion=1,
                     flag=wx.RIGHT|wx.LEFT,border=5)
        prog_box.Add(self.download_btn,proportion=0,border=5,
                     flag=wx.RIGHT|wx.LEFT)
        prog_box.Add(self.cancel_btn, proportion=0, border=5,
                      flag=wx.RIGHT|wx.LEFT)
        prog_box.Add(close_btn, proportion=0,border=5,
                     flag=wx.LEFT)

        #--------------------------------------------------------------------------
        #container for introsizer and Containers #1,#2,#3,#4,#5
        #-------------------------------------------
        self.main_container = wx.BoxSizer(wx.VERTICAL)
        sub_container_two.Add(url_box,proportion=0,flag=wx.EXPAND)
        sub_container_two.Add(dir_box,proportion=0,flag=wx.EXPAND)
        sub_container_two.Layout()
        self.main_container.Add(self.introsizer,proportion = 0,
                                flag=wx.EXPAND|wx.ALL, border=1)
        self.main_container.Add(self.hbox,proportion=0,flag=wx.EXPAND)
        self.main_container.Hide(self.hbox)
        self.panel.Layout()
        self.main_container.Add(Static_box,proportion=1,
                           flag=wx.EXPAND)
        self.main_container.Add(feature_box,proportion=0)
        self.main_container.Add(prog_box,proportion=0)
      
        panel.SetSizer(self.main_container)
        self.win.CenterOnScreen()
        #--------------------------------------------------------------------------
        
        #an empty list for showing filtered links.
        self.filtered = []
        #to take note of checkboxes checked or unchecked
        self.checked_boxes = []
        #for Select_All method, to keep track of checked items
        self.checked_items = []
        #to keep urls that were filtered manually, if default was unchecked
        self.preserve_filter = []
        #List for checked links to download;
         #used in (Enter),(Filter),(Evt_Check_Box)
        self.countLink = 0

        #---------------------------creating menubar-------------------------------
        menu = Menu(self.win)
        
    #------------------------------------------------------------------------------------
    def Evt_Check_Box(self, event):
        '''
        Event fired on checking any of check box.
        '''
        check_box = event.GetEventObject()
        regex = check_box.GetLabelText()                      #creating a regex pattern based on
                                                                #the label str of selected checkbox.
        try:            
            if event.IsChecked():
                #if box is checked, append its label to global checked boxes list
                self.checked_boxes.append(regex)
   
            else:
                #otherwise, remove it from there
                self.checked_boxes.remove(regex)

            #calling for applying filter according to current selected checkbox
            self.Filter()

            if self.select_all.IsChecked():
                #if select all was checked before current checkbox,
                 #add checkes to current selection too.
                self.Select_All()
                                    
        except Exception as e:
            print e
            
    #------------------------------------------------------------------------------------
    def Select_All(self, *event):
        '''
        Method called when select_all is checked.
        '''
        if self.select_all.IsChecked():
            if self.filtered:
                #if a filtered list exists, check all its items.
                 try:
                    self.checked_items = self.filtered
                    indices = range(len(self.filtered))
                    self.check_list.SetChecked(indices)
                 except Exception as e:
                     print e
            else:
                #else, check all items from found urls.
                try:
                    self.checked_items = self.urls
                    indices = range(len(self.urls))
                    self.check_list.SetChecked(indices)
                except Exception as e:
                    print e
        else:
            try:
                for index in xrange(len(self.checked_items)):
                    self.check_list.Check(index,False)
            except:
                pass
            
    #------------------------------------------------------------------------------------
    def Select_Default(self, event):
        '''
        Method for applying default filters.
        '''
        if event.IsChecked():
            #disable all other filters
            self.filter_btn.Disable()
            self.Enable_Checkes(False)
            self.regex.SetEditable(False)

            #call for applying current selected filters.
            self.Filter()
            if self.select_all.IsChecked():
                self.Select_All()

            self.panel.Layout()
        else:
            #enable all other filters
            self.filter_btn.Enable()
            self.Enable_Checkes(True)
            self.regex.SetEditable(True)

            self.main_container.Show(self.hbox)            
            self.panel.Layout()
            
            self.box.SetLabel("")
            if self.checked_boxes:
                #if any filter was applied before applying default; then apply that now.
                if not self.preserve_filter:
                    self.box.SetLabel("No links matched, try another filter; or to show all links, click 'show links' button")
                    self.main_container.Hide(self.hbox)

                self.filtered = self.preserve_filter
                self.check_list.SetItems(self.filtered)
                self.count.SetLabel("No. of links found: "+str(len(self.filtered)))
            
            else:
                self.check_list.SetItems(self.urls)
                self.count.SetLabel("No. of links found: "+str(self.countLink))

            if self.select_all.IsChecked():
                self.Select_All()                   
                               
    #------------------------------------------------------------------------------------
    def Enter(self, event):
        '''
        The method to prepare a list of all urls found on home page,
        '''
        #--------------------Fetching urls-----------------------------
        home_url = self.url_field.GetValue().strip()
        if home_url == "":
            self.url_field.SetValue("Please enter url")
            return

        #------------------saving history------------------------------
        if (class_preferences.OPTION_SELECTED == 
            class_preferences.HISTORY_OPTIONS[0]):
            utils.write_history(self.url_field.GetValue())

        #------------------fetching urls-------------------------------            
        self.box.SetLabel("Fetching...")
        wx.BeginBusyCursor()

        #--------------calling get_urls--------------------------------
        error, self.urls = get_urls.main(home_url)
        wx.EndBusyCursor()

        #-----------------compiling results----------------------------
        if self.urls:
            #-----------------if urls fetched--------------------------
            self.countLink = len(self.urls)
            
            self.main_container.Show(self.hbox)

            #------------Enabling the checkboxes, and buttons----------
            self.Enable_Checkes(True)
            self.select_default.Enable(True)

            self.filter_btn.Enable()
            self.regex.SetEditable(True)

            #----------------Creating check list box-------------------
            try:
                #if already exist, destroy that.
                self.check_list.Destroy()
                self.filtered = []
            except:
                pass

            self.check_list = wx.CheckListBox(self.panel, -1, (5,140),
                                              (490,120),self.urls,
                                              style = wx.HSCROLL)
            self.count.SetLabel("No. of links found: "+str(self.countLink))
            self.box.SetLabel("")
            
            self.bsizer.Add(self.check_list,proportion=1,flag=wx.EXPAND
                      |wx.ALL,border=2
                      )
                      
            self.panel.Layout()
            self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.Evt_Check_List_Box)
        else:
            print error
            dlg = wx.MessageDialog(self.panel,str(error),
                                       'Oops!', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            
    #------------------------------------------------------------------------------------
    def Filter(self,*event):
        '''
        The method filters links found on the page.
        It uses regex to filter and display a list of urls matching the pattern.
        The pattern is specified in the box called regex.
        '''
        global FILTERS
        
        #----------------------if default filter applied------------------------
        pattern = self.Make_Pattern()
            
        try:
            filtered = None
            if pattern:
                #--------------if any filter is applied.------------------------
                filtered = re.findall(pattern,'\n'.join(self.urls),re.I|re.M)
                self.filtered = filtered

                if self.filtered:
                    self.box.SetLabel("")
                    self.main_container.Show(self.hbox)
                    self.count.SetLabel("No. of links found: "+str(len(self.filtered)))
                else:
                    self.box.SetLabel("No links matched, try another filter; or to show all links, click 'show links' button")
                    self.main_container.Hide(self.hbox)

                self.check_list.SetItems(self.filtered)                   

            else:
                #-------------------else, show all urls------------------------
                self.filtered = []
                self.box.SetLabel("")
                self.main_container.Show(self.hbox)
                self.check_list.SetItems(self.urls)
                self.count.SetLabel("No. of links found: "+str(self.countLink))

            if self.select_all.IsChecked():
                self.Select_All()
           
            self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.Evt_Check_List_Box) 
        except Exception as e:
            print e
        
    #------------------------------------------------------------------------------------
    def Download(self,event):
        '''
        The method is bound with download button and download the content.
        It fetches urls from the check_list and sends urls to
        downloader_script.
        Uses 'browse' filedialog's path to save files.
        '''
        global DEFAULT_DIR

        #----------------collecting home_url----------------------------------------
        home_url = self.url_field.GetValue()
        if not(home_url == ""):      
            #If url field is not empty
            if self.dir.GetValue() == '':
                self.dir.SetValue("Please select location")
                return

            self.path = self.dir.GetValue()

            #-------------------start downloading process--------------------------
            wx.BeginBusyCursor()
            self.box.SetLabel("Fetching Information.....")
            self.cancel_btn.Enable()
                
            try:
                #get all checked links
                urls_to_download = self.check_list.GetCheckedStrings()

                if not urls_to_download:
                    #If no link selected, assume the home_url to download
                    urls_to_download = [home_url]

                #-----------------write download history--------------------------
                utils.write_downloads(urls_to_download,False)

                #-----------------call downloader script--------------------------
                error = downloader_script.main(urls_to_download,self.path,
                                               self.progress)

            except AttributeError:
                utils.write_downloads([home_url],False)            
                error = downloader_script.main([self.url_field.GetValue().strip()],self.path,
                                               self.progress)

            if error:
                print error
                dlg = wx.MessageDialog(self.panel,str(error),
                                       'Oops!', wx.OK|wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.box.SetLabel("Done")
            wx.EndBusyCursor()            
        else:
            self.url_field.SetValue("Please Enter url")

    #------------------------------------------------------------------------------------
    def Browse(self,event):
        '''
        The method is bound with the browse button.
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
            self.path = dlg.GetPath()
            self.dir.SetValue(self.path)

        dlg.Destroy()
        
    #------------------------------------------------------------------------------------
    def Reset(self,*event):
        '''
        This is bound to reset button, when pressed, it resets all widgets.
        '''
        self.url_field.SetValue(" ")
        self.url_field.SetFocus()
        try:
            self.check_list.Destroy()
        except Exception:
            pass
        self.regex.SetValue(" ")
        self.path = " "
        self.box.SetLabel("The links will be shown here")
        self.main_container.Hide(self.hbox)
        
        #Disabling all checkboxes
        self.Enable_Checkes(False)
        self.cb1.SetValue(False)
        self.cb2.SetValue(False)
        self.cb3.SetValue(False)
        self.cb4.SetValue(False)
        self.cb5.SetValue(False)
        self.cb6.SetValue(False)
        self.cb7.SetValue(False)
        self.cb8.SetValue(False)
        self.cb9.SetValue(False)
        self.select_all.SetValue(False)
        self.select_default.Enable(False)
        
        #disable unnecessary buttons
        self.cancel_btn.Disable()        
        self.filter_btn.Disable()        
        self.regex.SetEditable(False)
        self.progress.SetValue(0)
        self.win.Refresh()
        
        self.panel.Layout()

    #------------------------------------------------------------------------------------
    def Cancel(self, event):
        '''
        Method to cancel an on-going download.
        '''
        #sends stop interrupt to downloader script
        downloader_script.STOP = True
        dlg = wx.MessageDialog(self.panel,"Download canceled",
                                       'Oops!', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    #------------------------------------------------------------------------------------
    def Close(self, event):
        '''
        Method to close window.
        '''
        self.win.Destroy()

    #------------------------------------------------------------------------------------
    def Enable_Checkes(self,check=None):
        '''
        Method for checking or un-checking check-boxes.
        '''
        if check:
            self.cb1.Enable(True)
            self.cb2.Enable(True)
            self.cb3.Enable(True)
            self.cb4.Enable(True)
            self.cb5.Enable(True)
            self.cb6.Enable(True)
            self.cb7.Enable(True)
            self.cb8.Enable(True)
            self.cb9.Enable(True)           
        else:
            self.cb1.Enable(False)
            self.cb2.Enable(False)
            self.cb3.Enable(False)
            self.cb4.Enable(False)
            self.cb5.Enable(False)
            self.cb6.Enable(False)
            self.cb7.Enable(False)
            self.cb8.Enable(False)
            self.cb9.Enable(False)
    #------------------------------------------------------------------------------------
    def Evt_Check_List_Box(self, event):
        '''
        Method to implement checking and unchecking of list items.
        '''
        index = event.GetSelection()
        label = self.check_list.GetString(index)
        status = 'un'
        string_at_index = self.check_list.GetString(index)
        
        if self.check_list.IsChecked(index):
            status = ''
            self.check_list.SetSelection(index)        #so that (un)checking also selects

    #------------------------------------------------------------------------------------
    def Make_Pattern(self):
        '''
        Method to prepare a pattern to be filtered by filter method.
        '''
        pattern = None

        if self.select_default.IsChecked():
            #if default is selected, and any other filter is applied already, preserve
             #the current applied filter's result to re-apply when default is unchecked.
            self.preserve_filter = self.filtered
            self.filtered = []
            pattern = FILTERS
           
        else:           
            if (self.checked_boxes and
                not(self.checked_boxes[0] == self.checked_boxes[-1] == 'regex')):
                pattern = '.*\.'
                for i,pat in enumerate(self.checked_boxes):
                    if i == 0:
                        pattern += pat
                    else:
                        pattern += '|.*\.'+pat
                pattern += '.*'

            regex = self.regex.GetValue()
            
            if regex:
                self.checked_boxes.append('regex')
                if pattern:
                    pattern += '|'+ regex
                else:
                    pattern = regex
            elif 'regex' in self.checked_boxes:
                self.checked_boxes.remove('regex')

        return pattern         
    #------------------------------------------------------------------------------------
    
#--------------------------------------------------------------------------------------------

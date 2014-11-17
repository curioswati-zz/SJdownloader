'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''This script is used to download content from webpages
It Download the content from provided url.

It imports:
  -urllib
  
It defines:
  -main
  -extract_name
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Required modules'''
import urllib
import wx
from wx.lib.agw import pygauge as PG

def extract_name(url):
    """
    Extracts the name of the content item from provided url.
    """
    name = ""                         
    for ch in url[-1::-1]: 
        if ch == "/":                                                 #extracting from last field separated by "/"
            break
        name+=ch
        
    return name[-1::-1]
            
def main(urls, path,progress_bar):
    #When called with direct url
    stop = False
    print urls
    if (not(urls[0].startswith("http"))
        and ".html" not in urls[0]):
        return "Invalid url"

    total_size = 0

    for url in urls:
        connection = urllib.urlopen(url)
        meta = connection.info()
        try:
            size = meta.getheaders("content-length")[0]
            total_size += int(size)
        except IndexError:
            size = len(connection.read())
            total_size += size

    percent = total_size / len(urls)
    total_size /= float(1024)
    print str(total_size) + "Mb selected for download"
    #progress bar attributes
    progress_bar.SetValue([0,total_size])
    progress_bar.SetBarColor([wx.Colour(162,255,178),wx.Colour(159,176,255)])
    progress_bar.SetBackgroundColour(wx.WHITE)
    progress_bar.SetBorderColor(wx.BLACK)
    progress_bar.SetBorderPadding(2)
    progress_bar.SetDrawValue(draw=True, drawPercent=True, font=wx.SMALL_FONT, colour=wx.BLUE)
    progress_bar.Update([percent,0],2000)

    
    print "Downloading into "+path+" ..."
    for url in urls:
        name = extract_name(url)
        try:
            data = urllib.urlopen(url).read()
            save_file = open(path+"/"+name, 'wb')
            save_file.write(data)
            save_file.close()
            print name

#            download_size = len(data)
#            percent = download_size / float(total_size)           
            if stop:
                break
        except IOError as e:
            return e
            return "The connection could not establish."
            
if __name__ == "__main__":
    main(url,dir_)

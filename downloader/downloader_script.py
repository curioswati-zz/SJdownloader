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
            
def main(urls, path,panel,container):
    #When called with direct url
    if (not(urls[0].startswith("http"))
        or ".html" not in urls[0]):
        return "Invalid url"

    print "Downloading into "+path+" ..."
    for url in urls:
        name = extract_name(url)
        try:
            data = urllib.urlopen(url).read()
            save_file = open(path+"/"+name, 'wb')
            save_file.write(data)
            save_file.close()

            print 'Progress bar'
            progress_bar = PG.PyGauge(panel,-1,size=(100,25),style=wx.GA_HORIZONTAL)
            container.Add(progress_bar)
            print "Added pro_bar"
            progress_bar.SetValue([20,80])
            progress_bar.SetBarColor([wx.Colour(162,255,178),wx.Colour(159,176,255)])
            progress_bar.SetBackgroundColour(wx.WHITE)
            progress_bar.SetBorderColor(wx.BLACK)
            progress_bar.SetBorderPadding(2)
            progress_bar.SetDrawValue(draw=True, drawPercent=True, font=wx.SMALL_FONT, colour=wx.BLUE)

            progress_bar.Update([30,0],2000)
        except:
            return "The connection could not establish."
            
if __name__ == "__main__":
    main(url,dir_)

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
            
def main(urls, path):

    #print "Downloading into "+path+" ..."
    for url in urls:
        name = extract_name(url)
        #print name
        try:
            data = urllib.urlopen(url).read()
            save_file = open(path+"/"+name, 'wb')
            save_file.write(data)
            save_file.close()
        except:
            return "The connection could not establish."
            
if __name__ == "__main__":
    main(url,dir_)

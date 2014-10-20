'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''This script is used to download images from webpages
It Download all the images available on the input url page,
It takes input as a url.

It imports:
  -urllib
  -os
  
It defines:
  -main
  -extract_name
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Required modules'''
import os, urllib

def extract_name(url):
    """
    Extracts the name of the image form provided url.
    """
    name = ""                         
    for ch in url[-1::-1]: 
        if ch == "/":                                                 #extracting the name of image from last field separated by "/"
            break
        name+=ch
        
    return name[-1::-1]
            
def main(urls, path):

    print "Downloading into "+path+" ..."
    for url in urls:
        name = extract_name(url)
        print name
        try:
            data = urllib.urlopen(url).read()
            save_file = open(path+"/"+name, 'wb')
            save_file.write(data)
            save_file.close()
        except:
            print "The connection could not establish"
            
if __name__ == "__main__":
    main(url,dir_)

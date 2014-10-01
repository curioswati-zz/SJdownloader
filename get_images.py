'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''This script is used to download images from webpages
It Download all the images available on the input url page,
It takes input as a url.

It imports:
  -urllib
  -os
  
It defines:
  -main
  -get_image_url
  -get_images
  -extract_name
  -get_page''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Required modules'''
import os, urllib

def get_image_url(page):
    """ 
    Returns image urls found on page. 
    """
    start = page.find("src=")                                           #recognize image with src tag
    if start == -1:                                                     #if no src found
        return None,0
    url_start = page.find('"',start+1)                                
    url_end = page.find('"',url_start+1)
    url = page[url_start:url_end]                                       #extracting the url from src
    return url,url_end

def get_images(home_url,page,path):
    """
    Downloads images using image_urls found on page. 
    """
    while True:
        url,end = get_image_url(page)
        if url:
            if url.endswith(".jpg") or url.endswith(".jpeg"):
                if not url.startswith("http"):                           #if url was referenced from home_url; 
                    url = home_url+url[2:]                               #add that
                name = extract_name(url)                                 #extracting name of the image
                print name
                urllib.urlretrieve(url,path+"/"+name)                    #saving the image, while opening
            page = page[end:]                                            #moving forward in the page
        else:   
            break

def extract_name(url):
    """
    Extracts the name of the image form provided url.
    """
    name = ""                         
    for ch in url[-1::-1]: 
        if ch == "/":                                                   #extracting the name of image from last field separated by "/"
            break
        name+=ch
        
    return name[-1::-1]
            
def get_page(page):
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ''This module calls urlopen to collect the content of the input
    page from web.
    then returns that content to calling function.
    If any network error occurs and page is not fetched, it provides
    the user with suitable message.''
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    try:
        return urllib.urlopen(page).read()
    except:
        print "There was some problem fetching the file."
        return None

def main(home_url,dir_):

    if not os.path.isdir(dir_):                                          #creating directory specified by input
        os.mkdir(dir_)

    page = get_page(home_url)                                            #fetching content of page, so that, we can collect image urls from page.
    if page:
        print "Downloading..."
        get_images(home_url,page,dir_)                                   #downloading images from home_url
    else:
        print "There were no images on "+url
    return
            
if __name__ == "__main__":
    main(url,dir_)

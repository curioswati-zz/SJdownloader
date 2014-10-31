'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This script collects all the urls from input page.
It takes input as a url. and returns a list of all the urls found.''

It imports:
  -urllib

It defines:
  -main
  -get_page
  -get_all_links
  -get_next_url
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Required modules'''
''''''''''''''''''''''''''
import urllib
            
def get_next_url(page):
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ''This module finds the first url from the input page.
    where the href tag is found, is the starting of url.
    from the double qoutes, it finds end of the url.
    In the same way, it extracts src tags to find image and video urls.
    Finally returns the url and src, and its end point.
    returns none and 0, if both the href and src are not found.''
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    start_link = page.find('href=')                    #to find if any url exist.
    start_src = page.find('src=')                      #to find if any src exist.

    #setting default, for when nothing found
    url_end = 0
    src_end = 0
    url = src = None

    if start_link != -1:        
        start_url_at = page.find('"',start_link+1)     #starting of the url string.
        url_end = page.find('"',start_url_at+1)        #end of the url string. 
        url = page[start_url_at+1:url_end]             #the url.

    if start_src != -1:        
        start_src_at = page.find('"',start_src+1)      #starting of the src string.
        src_end = page.find('"',start_src_at+1)        #end of the src string. 
        src = page[start_src_at+1:src_end]             #the src.

    if url_end < src_end:                              #whichever occurs first.
        end = url_end
    else:
        end = src_end

    return url,src, end                                

def get_all_links(page,home_url):
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ''This module collects all urls from the input page
    It calls get_next_target to get a url in the page.
    one by one collects urls and return a list of them.''
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    urls = []
    while True:
        url, src, end_pos =  get_next_url(page)        #collecting the urls and the position on the page, where url ends.
        
        if url:                                        #if url was found.
            if (not url.startswith("http")
                and not url.startswith("https")):      #if url is referenced from home page, then adding that to
                url = home_url+url                     #the starting of url.

            if url not in urls:
                urls.append(url)

        if src:                                        #if src was found.
            if src.startswith('//'):
                src = 'http:'+src
            
            if (not src.startswith("http")
                and not src.endswith('js')             #when its not a javascript of css file.
                and not src.endswith('css')):
                src = home_url+src

            if src not in urls:
                urls.append(src)                       #creating entry in the list.
            
        page = page[end_pos+1:]                        #extracting the remaining part of the page after the end_pos.
        if not url and not src:                        #no urls or srcs were found. 
            break
    return urls

def get_page(page):
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ''This module calls urlopen to collect the content of the input
    page from web.
    then returns that content to calling function.
    If any network error occurs and page is not fetched, it provides
    the user with suitable error message.''
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    try:
        return (urllib.urlopen(page).read(), None)
    except:
        return (None, "There was some problem fetching the file.")

def main(home_url):

    page, error = get_page(home_url)
    if page:
        return (None, get_all_links(page,home_url))    #all the urls found on the page and none for error. 
    else:
        return (error, None)                           #error and none for urls.
 

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:07:14 2015

@author: cp
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

inputfile = open("urlfile.txt", 'rb')
data = inputfile.read() #read file
URLS = filter(None, data.splitlines()) #split on lines and remove white spaces
    

# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    session = requests.Session()
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp

# We can use a with statement to ensure threads are cleaned up promptly
with ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('\n %r generated an exception: %s' % (url, exc))
        else:
            print('\n%r page is %d bytes' % (url, len(data.content)))
            #test if content type is an image, print a warning if not
            if data.headers['content-type'].split('/')[0] != 'image':
                print("Warning: Content type is not an image. Content type: %r" % (data.headers['content-type']))
                
#todo:                
#number of succesfully loads
#hereof X number of not an image warnings
#number of unsuccesfully loads      
#load images
#logfile                
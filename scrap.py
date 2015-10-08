# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 13:55:39 2015

@author: cp
"""

import sys
import urllib, urllib2

def scrap(input_file):
    #open file containing urls, if file doesn't exist a IOError is automatically raised
    urlfile = open(str(input_file),'r')
    
    for url in urlfile:
        url = url.strip() #remove leading and trailing white space        
        #test if the url exists:        
        try:
            urllib2.urlopen(urllib2.Request(url))
       
        except:
            print str(url) + " does not exist"
            
        else:
            name = url.rsplit('/',1)[1] #image name extracted from url
            urllib.urlretrieve(url, name) #save url in local folder       
        
    urlfile.close() #close file 

if __name__ == "__main__":
   scrap(sys.argv[1])


"""
QUESTIONS:
check for inclusion of dependecies (import ....)
iterator vs. generator
overwriting in line 16 good style?
extract name or some customer file name option?
main blabla?
header
"""
Scrap.py is compatible with Python 2.7.
Scrap.py downloads images  to the local hard drive from an input textfile containing urls.
It saves a logfile (log.txt) containing the status for each url. Image downloads and log.txt are saved to the same folder as scrap.py.

To dremonstrate scrap.py use the test file 'urlfile.txt' as input argument, and make the following call from the the folder containing 
scrap.py and urlfile.txt:
C:\folder\containing\scrap.py\and\urlfile.txt> python scrap.py urlfile.txt

Scrap.py is dependent on the following packages:
requests
concurrent.futures
urlparse
itertools
datetime
re
click
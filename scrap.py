import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
#from urllib.parse import urlparse
from urlparse import urlparse
from itertools import groupby, chain
from datetime import datetime
import re
import click


#Returns the response given an url
def load_url(url, timeout=30, session=None, **kwargs):
    #test if session is given, if yes we do not want to spend time opening a new
    if session is None:
        session = requests.Session()
    resp = session.get(url, timeout=timeout, **kwargs)
    resp.raise_for_status()
    return resp


#This function parallellize calls to load_url() for each url in a group with same hostnames
#yields tuple (url, response) or (url, error)
def _get_batch(urls, threads=6, **kwargs):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        #make dictionary future: url
        future_to_url = {executor.submit(load_url, url, **kwargs):
                         url for url in urls}
        for future in as_completed(future_to_url):
            try:
                yield (future_to_url[future], future.result())
            except Exception as exc:
                yield (future_to_url[future], exc)


#This function yields lists of urls with similar hostname
#Input: list of abritatry urls
def _group_on_hostname(urls):
    urls = [urlparse(url) for url in urls]
    urls = sorted(urls, key=lambda o: o.hostname)
    for k, g in groupby(urls, key=lambda o: o.hostname):
        yield [o.geturl() for o in g]


#This function parallellize calls to _get_batch() for each hostname group of urls
#Returns a iterable (chain) containing the tuples (url, response) yielded from _get_batch
def _get_urls(urls, **kwargs):
    res = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        #make dictionary future: host group
        future_to_group = {executor.submit(_get_batch, group, session=requests.Session(), **kwargs): 
                           group for group in _group_on_hostname(urls)}
        for future in as_completed(future_to_group):
            res = chain(res, future.result()) 
    return res

#Write reponse status to the log file saved
def write_to_log(url, o, **kwargs):
    with open('log.txt', 'a') as log:
        if isinstance(o, Exception):
            log.write('Error: {} generated an exception: {}\n'.format(url, o))
        else:
            _safe_file(o, **kwargs)
            log.write('Saved:{} page ({} bytes)\n'.format(url, len(o.content)))
            #test if content type is an image, print a warning if not
            if o.headers['content-type'].split('/')[0] != 'image':
                log.write("WARNING: {} is NOT identified as an image. Content type: {}\n".format(url, o.headers['content-type']))

#save image to hard drive            
def _safe_file(o,count,n_urls):
    name = str(count).zfill(n_urls) 
    ext = '.' + list(filter(None, re.split("[/;]+", o.headers['content-type'])))[1]
    with open(name+ext, 'wb') as download:
                download.write(o.content)    
                
            


@click.command()
@click.argument('inputfile', type=click.File('rb'))

def run(inputfile):
    """This script downloads images from an input textfile containing urls to the local hard drive.
    It also saves a log.txt file containing the status for each url. Dovnloads and log.txt are saved to the same location as 
    this file."""
    data = inputfile.read() 
    urls = filter(None, data.splitlines()) #split on lines and remove white spaces
    count = 1
    with open('log.txt', 'w') as log:
        log.write('Logfile created: {} \n\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    for r in _get_urls(urls, timeout=2):
        print("Url no. {}: {}".format(count,r[0]))
        write_to_log(*r, count=count, n_urls=5)
        count = count + 1

if __name__ == "__main__":
    run()
    
#! /usr/bin/python
import httplib2
import urllib
import sys
from bs4 import BeautifulSoup
import re

def fetchGoogleQuery(query, offset=0):
    """
    Returns a tuple of http headers and html of google's response to a query
    """
    h = httplib2.Http()
    #make it look like this is from a browser
    headers = {
        'Accept':'text/html;level=1,text/plain;q=0.5',
        'Accept-Charset':'utf-8;q=0.8',
        'Accept-Language':'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Connection': 'keep-alive',
        'X-Chrome-Variations': 'CMu1yQEIkbbJAQigtskBCKW2yQEIqLbJAQiptskBCLK2yQEIsIPKAQ==',#this is from my browser, might want to change so I don't get blocked from google search on accident
        'Referer': 'http://www.google.com',
        'Cookie':'PREF=ID=9afe6519d1de20d1:FF=0:TM=1352086894:LM=1352086894:S=0szTLEfVNo6zV4MD; NID=65=p5E_1H6KJqLLsBIdzp3RWv2T1IHVV07aeWtj7-2SM-wvUPF-AR9l1YkA1z7ePuEnDQZkn7AHnW9qE8mM6WSUv10wCPs7Lla4wmzcyI-542toim3xsbUqcYjYbfYGHJZI' # cookies from freshly cleared not signed in google search without javascript enabled
    }
    if offset == 0:
        uri = "http://www.google.com/search?sclient=psy-ab&hl=en&site=&source=hp&q=%s&btnK=Google+Search" % urllib.quote_plus(query)
    else:
        uri = "http://www.google.com/search?hl=en&site=&prmd=ivns&start=%d&sa=N&q=%s" % (offset, urllib.quote_plus(query))

    headers, content = h.request(uri, "GET", headers=headers)
    return (headers, content)

def queryGoogle(query, results=10):
    """
    Searches google for query string, returns at least results number, possibly more 
    return list of tuples of (link, title, description)
    """
    retList, fetched = ([], 0)
    linkGroupRe = re.compile(r'(<li class="g">.*?</li>)')
    while fetched < results:
        headers, content = fetchGoogleQuery(query, offset=fetched)
        resultsRaw = linkGroupRe.findall(content) 

        for res in resultsRaw:
            soup = BeautifulSoup(res)
            site = soup.find('a', 'l')
            desc = soup.find('span', 'st')
            if site is not None and desc is not None:
                title = ''.join([unicode(x) for x in site.contents])
                body = ''.join([unicode(x) for x in desc.contents])
                retList.append((site['href'], title, body))
        fetched = len(retList)
    return retList


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print queryGoogle(sys.argv[1], results=20)



    


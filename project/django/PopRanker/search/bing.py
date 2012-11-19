import base64, urllib2, urllib
import app_signin as a # put user credientials in here, don't add to repo
import json

def search(query, count=20):
    encQuery = urllib.quote_plus(query)
    url = 'https://api.datamarket.azure.com/Bing/SearchWeb/Web?Query=%%27%s%%27&$top=%d&$format=json' % (encQuery, count)
    request = urllib2.Request(url)
    b64 = base64.standard_b64encode('%s:%s'  % (a.user, a.key)).replace('\n', '')
    request.add_header('Authorization', 'Basic %s' % b64)
    result = urllib2.urlopen(request)
    rawData = result.read()
    results = json.loads(rawData)
    retList = []
    if "d" in results and "results" in results["d"]:
        for res in results["d"]["results"]:
            retList.append((res["Url"], res["Title"], res["Description"]))

    return retList
        

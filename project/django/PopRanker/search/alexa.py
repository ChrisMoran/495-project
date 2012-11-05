import httplib2
from xml.dom.minidom import parseString


def alexaRank(domain):
    """
    Queries the undocumented alexa api, don't get blocked!
    return 0 if can't get rank
    domain is google.com, no http or www

    Relevant info in sd tag, looks like
    <sd>
      <POPULARITY URL="google.com" TEXT="???" SOURCE="panel"/>
      <REACH RANK="1"/> <-- we should only pull this value for now
      <RANK DELTA="+1"/>
      <COUNTRY CODE="US" name="United States" RANK="1"/>
    </sd>
    """

    h = httplib2.Http('.cache')
    #make it look like this is from a browser
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset':'utf-8;q=0.8',
        'Accept-Language':'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Connection': 'keep-alive',
        'Cache-Control':'max-age=0'
    }

    headers, content = h.request('http://data.alexa.com/data?cli=10&url=%s' % domain, "GET", headers=headers)
    xml = parseString(content)
    reachTag = xml.getElementsByTagName('REACH')
    if len(reachTag) > 0:
        return reachTag[0].getAttribute('RANK')
    else:
        return 0
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print alexaRank(sys.argv[1])

from urlparse import urlsplit
import sys

my_tld_file = "tlds.txt"

def get_tlds(tld_file):
# load tlds, ignore comments and empty lines:
    tlds = set()
    with open(tld_file) as tld_file:
        for line in tld_file:
            if line[0] not in "/\n":
                tlds.add(line.strip())
    return tlds

def get_tokens_from_tlds(url, tlds):
    """Returns a 4 tuple of sub-domain, domain, port, path"""
    parsed = urlsplit(url)
    path_and_port = parsed[1].split(':')
    url_elements = path_and_port[0].split('.')
    # url_elements = ["abcde","co","uk"]

    domain = ""
    for i in range(-len(url_elements), 0):
        last_i_elements = url_elements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(last_i_elements) # abcde.co.uk, co.uk, uk
        wildcard_candidate = ".".join(["*"] + last_i_elements[1:]) # *.co.uk, *.uk, *
        exception_candidate = "!" + candidate

        # match tlds: 
        if (exception_candidate in tlds):
            domain =  ".".join(url_elements[i:]) 
        if (candidate in tlds or wildcard_candidate in tlds):
            domain =  ".".join(url_elements[i-1:])
            # returns "abcde.co.uk"
        
    if domain == "":
        raise ValueError("Domain not in global list of TLDs")

    subdomain = path_and_port[0].replace(domain, "").strip('.')
    return (subdomain, domain, parsed.port, parsed.path)

def tld_closure(tld_file):
    tlds = get_tlds(tld_file)
    def wrapped_tokens(url):
        return get_tokens_from_tlds(url, tlds)
    return wrapped_tokens

get_tokens = tld_closure(my_tld_file)
    


	


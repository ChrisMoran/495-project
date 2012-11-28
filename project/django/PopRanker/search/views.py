# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render, redirect
from urllib import quote, unquote 
from django.views.decorators.csrf import ensure_csrf_cookie

#import google
import bing
import alexa
import re
from search.models import Search, Rank, Vote, Click



def index(request):
    return render(request, 'search/index.html', {})

@ensure_csrf_cookie
def search(request):
    if 'query' in request.GET:
        q = request.GET['query']
        Search(query=q).save() # record search and timestamp
        results = bing.search(q, count=25)

        rankedResults = []
        for result in results:
            t = int(getAlexaRank(result[0]))
            rankedResults.append(result[:] + (t,))

        rankedResults.sort(key= lambda r: r[3], reverse=True)

        finalResults = []
        for rank, result in enumerate(rankedResults, 1):
            # for redirect
            url = '/click/?url=%s&rank=%d&search=%s' % (quote(result[0]), rank, q)
            # add orignial url on the end for voting mechanism
            finalResults.append((url,) + result[1:] + (quote(result[0]),))

        context = {'results': finalResults, 'query' : q }
    else:
        context = {}
    return render(request, 'search/search.html', context)


def getAlexaRank(url):
    """
    Checkes local cache is we already have seen this site, otherwise queries alexa
    """
    parts = url.split('/')
    try:
        cacheVal = Rank.objects.get(domain=parts[2])
        return cacheVal.rank
    except:
        if len(parts) > 2:
            rank = int(alexa.alexaRank(parts[2]))
            Rank(domain=parts[2], rank=rank).save()
            return rank
        else:
            return 0

def validVote(req):
    return ('query' in req.POST) and ('url' in req.POST) and ('vote' in req.POST)

def vote(req):
    if validVote(req):
        v = int(req.POST['vote']) == 1 
        Vote(query=req.POST['query'], link=unquote(req.POST['url']), vote=v).save()
    return HttpResponse("")

def click(req):
    if "url" in req.GET and "rank" in req.GET and "search" in req.GET:
        u = unquote(req.GET['url'])
        Click(url=u, search=req.GET['search'], rank=int(req.GET['rank'])).save()
        return redirect(u)
    return HttpResponse("Nothing to see here...")

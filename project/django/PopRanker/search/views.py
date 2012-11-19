# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render

#import google
import bing
import alexa
import re
from search.models import Search, Rank, Vote



def index(request):
    return render(request, 'search/index.html', {})

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
        context = {'results': rankedResults, 'query' : q }
    else:
        context = {}
    return render(request, 'search/search.html', context)

def searchajax(request):
    if 'query' in request.GET:
        q = request.GET['query']
        Search(query=q).save() # record search and timestamp
        results = bing.search(q, count=25)
        rankedResults = []
        for result in results:
            t = int(getAlexaRank(result[0]))
            rankedResults.append(result[:] + (t,))

        rankedResults.sort(key= lambda r: r[3], reverse=True)
        context = {'results': rankedResults, 'query' : q }
    else:
        context = {'error': 'error-data'}
    return HttpResponse(context)


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
        Vote(query=req.POST['query'], link=req.POST['url'], vote=v).save()
    return HttpResponse("")

def click(req):
    return HttpResponse("")

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render

import google
import alexa
import re
from search.models import Search, Rank, Vote


def index(request):
    return render(request, 'search/index.html', {})

def search(request):
    if 'query' in request.GET:
        q = request.GET['query']
        Search(query=q).save() # record search and timestamp
        results = google.queryGoogle(q, results=20)
        rankedResults = []
        for result in results:
            rankedResults.append((int(getAlexaRank(result[0])), result))

        rankedResults.sort(key= lambda r: r[0], reverse=True)
        context = {'results': [r[1] for r in rankedResults], 'query' : q }
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
        Vote(query=req.POST['query'], link=req.POST['url'], vote=v).save()
    return HttpResponse("")

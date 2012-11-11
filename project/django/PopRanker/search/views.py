# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render

import google
import alexa
import re
from search.models import Search, Rank


def index(request):
    return render(request, 'search/index.html', {})

def search(request):
    if 'query' in request.GET:
        Search(query=request.GET['query']).save() # record search and timestamp
        results = google.queryGoogle(request.GET['query'], results=20)
        rankedResults = []
        for result in results:
            rankedResults.append((int(getAlexaRank(result[0])), result))

        rankedResults.sort(key= lambda r: r[0], reverse=True)
        context = {'results': [r[1] for r in rankedResults] }
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

def vote(request):
    return HttpResponse("this isn't really a visiting page")

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render

import google
import alexa
from search.models import Search


def index(request):
    return render(request, 'search/index.html', {})

def search(request):
    if 'query' in request.GET:
        results = google.queryGoogle(request.GET['query'], results=20)
        context = {'results': results }
        #try:
        #    prevSearch = Search.objects.filter(query=request.GET['query']).order_by(timestamp)
            
        #except Search.DoesNotExist:
            # query google takes a long time, so cache results
            
    else:
        context = {}
    return render(request, 'search/search.html', context)

def vote(request):
    return HttpResponse("this isn't really a visiting page")

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render

def index(request):
    return render(request, 'search/index.html', {})

def search(request):
    return HttpResponse("totally searching dogg")

def vote(request):
    return HttpResponse("this isn't really a visiting page")

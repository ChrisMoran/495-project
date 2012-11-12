from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from search import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^search/$', views.search, name='seaerch'),
                       url(r'^vote/$', views.vote, name='vote')
)


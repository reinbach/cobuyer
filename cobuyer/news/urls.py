from django.conf.urls.defaults import *

from news import views

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)$', views.view, name='news_view'),
    url(r'^$', views.home, name='news_home'),
)
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from feeds import LatestEntries
from core import views

admin.autodiscover()

feeds = {
    'news': LatestEntries,
}

urlpatterns = patterns(
    '',
    (r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}),
    url(r'^news/', include('news.urls')),
    url(r'^product/', include('product.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^$', views.home, name='home'),
)

urlpatterns += staticfiles_urlpatterns()

handler500 = views.handler500
from django.conf.urls.defaults import *

from accounts import views

urlpatterns = patterns('',
    url(r'^login/$', views.login, name='account_login'),
    url(r'^logout/$', views.logout_user, name='account_logout'),
    url(r'^create/$', views.create, name='account_create'),
    url(r'^update/$', views.update, name='account_update'),
    url(r'^password/$', views.password, name='account_password'),
    url(r'^reset/$', views.reset_password, name='account_reset_password'),
    url(r'^$', views.home, name='account_home'),
)
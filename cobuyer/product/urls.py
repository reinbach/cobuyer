from django.conf.urls.defaults import *

from product import views

urlpatterns = patterns('',
    url(r'^category/(?P<category_code>\w+)$', views.by_category, name='product_category'),
    url(r'^search/$', views.search, name='product_search'),
    url(r'^$', views.list, name='product_list'),
)
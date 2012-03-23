from django.conf.urls.defaults import *

from cart import views

urlpatterns = patterns('',
    url(r'^add/(?P<product_id>\d+)$', views.add, name='cart_add'),
    url(r'^delete/(?P<item_id>\d+)$', views.delete, name='cart_delete'),
    url(r'^complete/$', views.complete, name='cart_complete'),
    url(r'^print/(?P<cart_id>\d+)$', views.print_cart, name='cart_print'),
    url(r'^(?P<cart_id>\d+)$', views.show_cart, name='cart_view'),
    url(r'^$', views.home, name='cart_home'),
)
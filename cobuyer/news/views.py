from django.shortcuts import get_list_or_404

from shortcuts import request_to_response

from news import models

#-------------------------------------------------------------------------------
def home(request):
    news_list = models.News.objects.all().order_by('-created')
    data = dict(
        news_list=news_list
    )
    return request_to_response(request, 'news/index.html', data)

#-------------------------------------------------------------------------------
def view(request, slug):
    news_item = get_list_or_404(models.News.objects, slug=slug)
    data = dict(
        news_list=news_list
    )
    return request_to_response(request, 'news/index.html', data)
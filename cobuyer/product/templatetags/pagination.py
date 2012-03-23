from django.conf import settings
from django.template import Library

register = Library()

#-------------------------------------------------------------------------------
@register.inclusion_tag('pagination.html')
def pagination(page, curpage, tags=''):
    return {'MEDIA_URL': settings.MEDIA_URL, 'page': page, 'curpage': curpage, 'tags': tags}

from django.contrib.syndication.feeds import Feed

from news import models

#===============================================================================
class LatestEntries(Feed):
    title = 'AssocBuyer Site News'
    link = '/news/'
    description = 'Updates on changes and additions to assocbuyer.reinbach.com'
    
    def items(self):
        return models.News.objects.order_by('-created')[:5]
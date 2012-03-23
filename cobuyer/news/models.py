from django.db import models

#===============================================================================
class News(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    
    #===========================================================================
    class Meta:
        verbose_name_plural = 'news'
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.title
    
    #---------------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        return ('news_view', (), {'slug': self.slug})

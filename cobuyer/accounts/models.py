from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

#===============================================================================
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    number = models.CharField(max_length=10, blank=True, null=True)
    group = models.ManyToManyField("self")
    group_leader = models.BooleanField(default=False)
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return '%s' % self.number
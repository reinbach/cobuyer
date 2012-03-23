from django.db import models
from django.db.models import permalink

#===============================================================================
class Brand(models.Model):
    label = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    #---------------------------------------------------------------------------
    def __unicode__(self):
        return '%s' % self.code

#===============================================================================
class Category(models.Model):
    label = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    #===========================================================================
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['label']
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return '%s' % self.code

    #---------------------------------------------------------------------------
    @property
    def get_label(self):
        return self.label if self.label else self.code
    
    #---------------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
        return ('product_category', (), {'category_code': self.code})
    
#===============================================================================
class Product(models.Model):
    item_number = models.CharField(max_length=20)
    brand = models.ForeignKey(Brand)
    description = models.CharField(max_length=250)
    size = models.CharField(max_length=20)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    unit_sale_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    total_sale_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category)
    upc_number = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    modified = models.DateTimeField(auto_now=True)
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return '%s: %s' % (self.item_number, self.description)

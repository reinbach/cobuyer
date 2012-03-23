from django.contrib import admin

from product import models

#===============================================================================
class BrandAdmin(admin.ModelAdmin):
    list_display = ('label', 'code', 'description', 'created', 'modified')
    search_fields = ('label', 'code')
    list_filter = ('label', 'code', 'created', 'modified')

admin.site.register(models.Brand, BrandAdmin)

#===============================================================================
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'code', 'description', 'created', 'modified')
    search_fields = ('label', 'code')
    list_filter = ('label', 'code', 'created', 'modified')
    
admin.site.register(models.Category, CategoryAdmin)
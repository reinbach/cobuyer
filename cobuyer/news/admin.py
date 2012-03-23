from django.contrib import admin

from news import models

#===============================================================================
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_filters = ('title', 'created')
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.News, NewsAdmin)
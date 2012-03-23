
from south.db import db
from django.db import models
from news.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'News'
        db.create_table('news_news', (
            ('id', orm['news.News:id']),
            ('title', orm['news.News:title']),
            ('slug', orm['news.News:slug']),
            ('body', orm['news.News:body']),
            ('created', orm['news.News:created']),
        ))
        db.send_create_signal('news', ['News'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'News'
        db.delete_table('news_news')
        
    
    
    models = {
        'news.news': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['news']

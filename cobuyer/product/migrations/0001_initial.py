
from south.db import db
from django.db import models
from product.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Brand'
        db.create_table('product_brand', (
            ('id', orm['product.Brand:id']),
            ('label', orm['product.Brand:label']),
            ('code', orm['product.Brand:code']),
            ('description', orm['product.Brand:description']),
            ('created', orm['product.Brand:created']),
            ('modified', orm['product.Brand:modified']),
        ))
        db.send_create_signal('product', ['Brand'])
        
        # Adding model 'Category'
        db.create_table('product_category', (
            ('id', orm['product.Category:id']),
            ('label', orm['product.Category:label']),
            ('code', orm['product.Category:code']),
            ('description', orm['product.Category:description']),
            ('created', orm['product.Category:created']),
            ('modified', orm['product.Category:modified']),
        ))
        db.send_create_signal('product', ['Category'])
        
        # Adding model 'Product'
        db.create_table('product_product', (
            ('id', orm['product.Product:id']),
            ('item_number', orm['product.Product:item_number']),
            ('brand', orm['product.Product:brand']),
            ('description', orm['product.Product:description']),
            ('size', orm['product.Product:size']),
            ('unit_price', orm['product.Product:unit_price']),
            ('total_price', orm['product.Product:total_price']),
            ('unit_sale_price', orm['product.Product:unit_sale_price']),
            ('total_sale_price', orm['product.Product:total_sale_price']),
            ('category', orm['product.Product:category']),
            ('upc_number', orm['product.Product:upc_number']),
            ('created', orm['product.Product:created']),
            ('modified', orm['product.Product:modified']),
        ))
        db.send_create_signal('product', ['Product'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Brand'
        db.delete_table('product_brand')
        
        # Deleting model 'Category'
        db.delete_table('product_category')
        
        # Deleting model 'Product'
        db.delete_table('product_product')
        
    
    
    models = {
        'product.brand': {
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'product.category': {
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'product.product': {
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'total_sale_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'unit_sale_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'upc_number': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['product']

#!/usr/bin/python
#
# script takes spreadsheet and load the products in the
# database
#
# for each row
# a. deactivate all specials for current products
# 1. create current brand list
# 2. create current category list
# 3. check that it is a product row
# 4. check if the brand exists
#    - if brand does not exist then create new brand 
#    - update the current brand list
# 5. check if category exists
#    - if category does not exist then create
#    - update the current category list
# 6. check if product already exists (use item_number to check against)
# 6a. if product exists then update
# 6b. otherwise add new product
#
import datetime

from django.core.management.base import BaseCommand, CommandError

import xlrd
from product import models

#===============================================================================
class Command(BaseCommand):
    help = 'Upload the Food Co-op excel document of products.'
    args = '[file]'
    label = 'file name'
    
    #---------------------------------------------------------------------------
    def handle(self, file='', **options):
        if file == '':
            raise CommandError('File is required')

        # remove all current specials
        for product in models.Product.objects.all():
            product.unit_sale_price = None
            product.total_sale_price = None
            product.save()
            
        brand_list = models.Brand.objects.values_list('code', flat=True)
        category_list = models.Category.objects.values_list('code', flat=True)

        book = xlrd.open_workbook(file)
        
        # we are only concerned with the first worksheet
        # as the second worksheet is the same in a different order
        sh = book.sheet_by_index(0)
        for rx in range(2,sh.nrows):
            # products all have a value in the 3rd column
            if sh.cell_value(rowx=rx, colx=3).strip() != '':
                item_number = sh.cell_value(rowx=rx, colx=1)
                brand = sh.cell_value(rowx=rx, colx=2)
                description = sh.cell_value(rowx=rx, colx=3)
                size = sh.cell_value(rowx=rx, colx=4)
                unit_price = sh.cell_value(rowx=rx, colx=5)
                total_price = sh.cell_value(rowx=rx, colx=6)
                unit_sale_price = sh.cell_value(rowx=rx, colx=7)
                total_sale_price = sh.cell_value(rowx=rx, colx=8)
                category = sh.cell_value(rowx=rx, colx=10)
                upc_number = sh.cell_value(rowx=rx, colx=11)
                
                # check if brand exists, if not add
                if brand in brand_list:
                    brand = models.Brand.objects.get(code=brand)
                else:
                    brand = models.Brand.objects.create(code=brand)
                    brand_list = models.Brand.objects.values_list('code', flat=True)
                
                #check if category exits, if not add
                if category in category_list:
                    category = models.Category.objects.get(code=category)
                else:
                    category = models.Category.objects.create(code=category)
                    category_list = models.Category.objects.values_list('code', flat=True)
                
                # check if product exists, otherwise add
                try:
                    prod = models.Product.objects.get(item_number='%s' % item_number)
                except models.Product.DoesNotExist:
                    prod = models.Product()
                
                prod.item_number = item_number    
                prod.brand = brand
                prod.description = description
                prod.size = size
                prod.unit_price = str(unit_price)
                prod.total_price = str(total_price)
                prod.category = category
                prod.upc_number = upc_number
                prod.active = True
                
                # sale prices may be empty convert to null if so
                if unit_sale_price != '':
                    prod.unit_sale_price = str(unit_sale_price)
                if total_sale_price != '':
                    prod.total_sale_price = str(total_sale_price)
                
                print '%s: %s' % (prod.item_number, prod.description)
                prod.save()
        # updated all products that have not been updated to in-active
        inactive_list = models.Product.objects.filter(
            modified__lt=datetime.datetime.today().strftime('%Y-%m-%d')
        )
        inactive_list.update(active=False)

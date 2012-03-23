import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink

import settings

from product import models as product

#===============================================================================
class Cart(models.Model):
    user = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return '%s' % self.user
    
    #---------------------------------------------------------------------------
    def total(self):
        items = Item.objects.filter(cart=self)
        total = 0
        for item in items:
            total += item.total
        return total
    
    #---------------------------------------------------------------------------
    def tax(self):
        return (float(self.total()) * float(settings.TAX_RATE) / 100.0)
    
    #---------------------------------------------------------------------------
    def shipping_charge(self):
        return (float(self.total()) * float(settings.SHIPPING_RATE) / 100.0)
    
    #---------------------------------------------------------------------------
    def total_grand(self):
        return self.total() + self.tax() + self.shipping_charge()
    
    #---------------------------------------------------------------------------
    def complete(self):
        """
        Mark cart as complete
        Only do this if the cart has some items associated with it
        """
        if Item.objects.filter(cart=self).count() > 0:
            self.completed = True
            self.save()


#===============================================================================
class Item(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(product.Product)
    description = models.CharField(max_length=250)
    size = models.CharField(max_length=20)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return '%s' % self.product
    
    #---------------------------------------------------------------------------
    def _lb_10_increment(self):
        """
        Check to see if qty is 10lb increment
        """
        if int(self.quantity) % 10 == 0:
            return True
        return False
    
    #---------------------------------------------------------------------------
    def _lb_5_increment(self):
        """
        Check to see if qty is 5lb increment
        """
        if int(self.quantity) % 5 == 0:
            return True
        return False
    
    #---------------------------------------------------------------------------
    def _get_unit_qty(self):
        """
        Ensure that the qty value is correct
        
        Always use product size value unless cart is completed then use cart 
        size value
        
        Qty is determined from size value and is calculated different if
        dealing with lbs as well as when it has * or ** characters
        
        * - means the item can be sold in 5lb increments
        If the value given is not a multilpe of 5 then take the qty value given
        to mean a multiple of the size value
        
        Example 1:
        Size value is 25# * and the qty value given is 5
        then we take this to mean 5lbs
        
        Example 2:
        Size value is 25# * and the qty value given is 3
        then we take this to mean 25 * 3 = 75lbs
        
        ** - means that the item can be sold in 10lb increments
        If the value given is not a multiple of 10 then take the qty value given 
        to mean a multiple of the size value
        
        Example 1:
        Size value is 50# ** and the qty value given is 10
        then we take this to mean 10lbs
        
        Example 2:
        Size value is 50# ** and the qty value given is 1
        then we take this to mean 50lbs
        
        / - means that the qty is a multiple of the leading number of the size
        Take the qty value given and multiply by the leading number of the size
        
        Example 1:
        Size value is 3/12 oz and the qty value given is 4
        then we take this to mean 3 * 4 = 12 qty

        For all other size values we take the qty value given to mean multiples
        of the size value
        
        Example 1:
        If the size value is 5# and the qty value given is 5
        then we take this to mean 25#
        """
        if self.cart.completed:
            size = self.size
        else:
            size = self.product.size
        non_decimal = re.compile(r'[^\d]+')
        qty = self.quantity
        try:
            # if there is a dash in the size value, we need to take the first number
            # and remove the - and last number from the size value for later
            # calculations
            if re.search('-', size):
                size = size.partition('-')[2]
            size_int = int(non_decimal.sub('', size))
        except ValueError, e:
            size_int = 1
        # 10 lb increments
        if re.search('\*{2}', size):
            if not self._lb_10_increment():
                qty = int(self.quantity) * size_int
        # 5 lb increments
        elif re.search('\*{1}', size):
            if not self._lb_5_increment():
                qty = int(self.quantity) * size_int
        elif re.search('\d+/', size):
            multiplier = size.partition('/')
            qty = int(multiplier[0]) * int(self.quantity)
        elif re.search('#', size):
            qty = int(self.quantity) * size_int
        return qty
        
    #---------------------------------------------------------------------------
    def _get_price(self):
        """
        Price is either sales price or unit price.
        If there is a sales price then use that otherwise use the unit price
        
        Always make use of the unit/sale price from the products table unless
        the cart is marked as complete then use the unit/sale price from the 
        cart table
        
        If the product unit/sale price differs from the cart price then update 
        the cart price. Only if the cart is not complete
        
        The unit price is always for a single unit of the item
        
        If the item is a 10lb increment or a 5lb increment then need to add 
        to the unit price. 15c extra for 10lb increments and 25c extra for 5lb 
        increments
        
        Example 1:
        Unit price is 1.13 and the size value is 25#
        then the 1.13 is per 1lb of the item
        
        Example 2:
        Unit price is 1.13 and the size value is 50# **
        and the qty selected is 10lb increment then add 15c to unit price
        So unit price is 1.13 + 0.15 = 1.28
        
        Example 3:
        Unit price is 0.90 and the size value is 25# *
        and the qty selected is 5lb increment then add 25c to unit price
        So unit price is 0.90 + 0.25 = 1.15
        
        Example 4:
        Unit price is 1.10 and the size value is 25# *
        and the qty selected is 25lb then we don't add anything to unit price
        So unit price is 1.10
        """
        if self.cart.completed:
            if self.sale_price:
                return self.sale_price
            else:
                return self.unit_price
        else:
            unit_increment = 0
            size = self.product.size
            if re.search('\*{2}', size):
                if self._lb_10_increment():
                    unit_increment = 0.15
            elif re.search('\*{1}', size):
                if self._lb_5_increment():
                    unit_increment = 0.25
            if self.product.unit_sale_price:
                unit_sale_price = float(self.product.unit_sale_price) + unit_increment
                if self.sale_price is None or unit_sale_price != float(self.sale_price):
                    self.sale_price = unit_sale_price
                    self.save()
                return unit_sale_price
            else:
                unit_price = float(self.product.unit_price) + unit_increment
                if unit_price != float(self.unit_price):
                    self.unit_price = unit_price
                    self.save()
                return unit_price

    #---------------------------------------------------------------------------
    def _total_price(self):
        return float(self.price) * float(self.qty)
    
    total = property(_total_price)
    price = property(_get_price)
    qty = property(_get_unit_qty)

from django import forms

from product import models as prod_model

from cart import models

#===============================================================================
class AddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='Qty',
        widget=forms.TextInput(attrs={'size': '3'}),
        initial=1
    )
    
    #---------------------------------------------------------------------------
    def __init__(self, request, cart, *args, **kws):
        super(AddProductForm, self).__init__(*args, **kws)
        self.request = request
        self.cart = cart
    
    #---------------------------------------------------------------------------
    def save(self, product_id):
        """
        Add the product to the cart
        """
        data = self.cleaned_data
        
        # check if product exist in cart already
        if models.Item.objects.filter(cart=self.cart, product__pk=product_id):
            return u'Product is already in the cart.'
        else:
            product = prod_model.Product.objects.get(pk=product_id)
            item = models.Item.objects.create(
                cart=self.cart,
                product=product,
                description=product.description,
                size=product.size,
                quantity=data['quantity'],
                unit_price=product.unit_price,
                sale_price=product.unit_sale_price,
            )
            return True
            

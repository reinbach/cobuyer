from django import forms

from product import models

#===============================================================================
class ProductSearchForm(forms.Form):
    item_number = forms.CharField(
        max_length=20, 
        required=False,
    )
    brand = forms.CharField(
        max_length=20, 
        required=False,
    )
    description = forms.CharField(
        max_length=50, 
        required=False,
    )
    category = forms.ChoiceField(
        required=False,
        choices=models.Category.objects.values_list('id', 'label')
    )
    
    #---------------------------------------------------------------------------
    def __init__(self, request, *args, **kws):
        super(ProductSearchForm, self).__init__(*args, **kws)
        self.request = request
        
        if ('', 'ALL') not in self.fields['category'].choices:
            self.fields['category'].choices.reverse()
            self.fields['category'].choices.append(('', 'ALL'))
            self.fields['category'].choices.reverse()
    
    #---------------------------------------------------------------------------
    def search(self, products):
        data = self.cleaned_data
        
        if data['item_number']:
            products = products.filter(
                item_number__icontains=data['item_number']
            )
        
        if data['brand']:
            products = products.filter(
                brand__code__icontains=data['brand']
            )
        
        if data['description']:
            products = products.filter(
                description__icontains=data['description']
            )
        
        if data['category']:
            products = products.filter(
                category__pk=data['category']
            )
        
        return products

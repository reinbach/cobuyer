from django.shortcuts import get_object_or_404
from django.core.paginator import InvalidPage, EmptyPage

from cart import forms as cart
from libs.pagination import DiggPaginator
from shortcuts import request_to_response

from product import models, forms

# pagination params
DIGG_ATTRS = dict(body=5, tail=2, padding=2, margin=2)
MAX_RESULTS = 50

#-------------------------------------------------------------------------------
def _render(request, template, data):
    data['category_list'] = models.Category.objects.all()
    data['form_add'] = cart.AddProductForm(request, None)
    
    try:
        data['form']
    except KeyError:
        data['form'] = forms.ProductSearchForm(request)

    return request_to_response(request, template, data)

#-------------------------------------------------------------------------------
def list(request):
    product_count = models.Product.objects.all().count()
    specials_count = models.Product.objects.filter(unit_sale_price__isnull=False).count()
    brand_count = models.Brand.objects.all().count()
    
    data = dict(
        product_count=product_count,
        brand_count=brand_count,
        specials_count=specials_count,
    )
    return _render(request, 'product/index.html', data)

#-------------------------------------------------------------------------------
def by_category(request, category_code):
    category = get_object_or_404(models.Category, code=category_code)
    products = models.Product.objects.filter(category=category).order_by('description')
    
    paginator = DiggPaginator(products, MAX_RESULTS, **DIGG_ATTRS)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try: 
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    
    data = dict(
        category=category,
        products=products,
        paginator=paginator,
        curpage=page,
    )
    
    return _render(request, 'product/list.html', data)

#-------------------------------------------------------------------------------
def search(request):
    products = models.Product.objects.all().order_by('description')
    
    if request.method == 'POST':
        form = forms.ProductSearchForm(request, data=request.POST)
        if form.is_valid():
            products = form.search(products)
    else:
        form = forms.ProductSearchForm(request)
    
    for product in products:
        product.form = cart.AddProductForm(request, None, product)

    paginator = DiggPaginator(products, MAX_RESULTS, **DIGG_ATTRS)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try: 
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    
    data = dict(
        products=products,
        paginator=paginator,
        curpage=page,
        form=form
    )
    
    return _render(request, 'product/list.html', data)
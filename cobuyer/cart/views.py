from django import http
from django.contrib.auth.decorators import login_required
from django.core.paginator import InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from cStringIO import StringIO
from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from shortcuts import request_to_response
from libs.pagination import DiggPaginator
import settings

from product import models as prod_model

from cart import models, forms, utils

# pagination params
DIGG_ATTRS = dict(body=5, tail=2, padding=2, margin=2)
MAX_RESULTS = 10

#-------------------------------------------------------------------------------
def _show_cart(request, cart, form=None):
    """
    Display the contents of the cart selected
    """
    products = models.Item.objects.filter(cart=cart).order_by('description')
    
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
        cart=cart,
        products=products,
        curpage=page,
        form=form,
        tax_rate=settings.TAX_RATE,
        shipping_rate=settings.SHIPPING_RATE
    )
    return request_to_response(request, 'cart/index.html', data)

#-------------------------------------------------------------------------------
@login_required(redirect_field_name='login')
@utils.get_cart
def home(request, cart):
    return _show_cart(request, cart)

#-------------------------------------------------------------------------------
@login_required(redirect_field_name='login')
@utils.get_cart
def add(request, cart, product_id):
    if request.method == 'POST':
        form = forms.AddProductForm(request, cart, data=request.POST)
        if form.is_valid():
            form.save(product_id)
    return http.HttpResponseRedirect(reverse('cart_home'))

#-------------------------------------------------------------------------------
@login_required(redirect_field_name='login')
@utils.get_cart
def delete(request, cart, item_id):
    models.Item.objects.get(pk=item_id).delete()
    return http.HttpResponseRedirect(reverse('cart_home'))

#-------------------------------------------------------------------------------
@login_required(redirect_field_name="login")
@utils.get_cart
def complete(request, cart):
    cart.complete()
    return http.HttpResponseRedirect(reverse('account_home'))

#-------------------------------------------------------------------------------
@login_required(redirect_field_name='login')
def show_cart(request, cart_id):
    cart = get_object_or_404(models.Cart, pk=cart_id, user=request.user)
    return _show_cart(request, cart)

#-------------------------------------------------------------------------------
@login_required(redirect_field_name="login")
def print_cart(request, cart_id):
    cart = get_object_or_404(models.Cart, pk=cart_id, user=request.user)
    items = models.Item.objects.filter(cart=cart).order_by('description')
    data = [[
        'Stock #', 
        'Brand', 
        'Item Description', 
        'Size', 
        'Qty', 
        'Price', 
        'Total'
    ]]
    for item in items:
        d = []
        d.append(item.product.item_number)
        d.append(item.product.brand)
        d.append(item.description)
        d.append(item.size)
        d.append(item.quantity)
        d.append('%.2f' % item.price)
        d.append('%.2f' % item.total)
        data.append(d)
    
    total_data = [
        ['Sub Total:', '%.2f' % cart.total()],
        ['Shipping Charge (%.0f%s):' % (settings.SHIPPING_RATE, '%'), '%.2f' % cart.shipping_charge()],
        ['Tax (%.0f%s):' % (settings.TAX_RATE, '%'), '%.2f' % cart.tax()],
        ['Total:', '%.2f' % cart.total_grand()],
    ]
    
    stylesheet = getSampleStyleSheet()
    heading = platypus.Paragraph(
        'Order - %s' % cart.modified.strftime("%m/%d/%Y"), 
        stylesheet['Heading1']
    )
    
    cart_items = platypus.Table(data)
    cart_items.setStyle(platypus.TableStyle([
        # amount columns (last 2)
        ('ALIGN', (5, 0), (-1, -1), 'RIGHT'),
        # qty column
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        # add title underline
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ]))
    
    cart_totals = platypus.Table(total_data)
    cart_totals.setStyle(platypus.TableStyle([
        # span cells for the totals at the bottom
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (0, 0), 378)
    ]))
    
    response = http.HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=order_%s.pdf' % cart.modified.strftime('%Y_%m_%d')
    
    buffer = StringIO()
    doc = platypus.SimpleDocTemplate(buffer)
    Story = [platypus.Spacer(1,0)]
    Story.append(heading)
    Story.append(cart_items)
    Story.append(cart_totals)
    doc.build(Story)
    
    # Get the value of the StringIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

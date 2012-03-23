from cart import models

#---------------------------------------------------------------------------
def get_cart(function):
    """
    Decorator gets latest cart
    """
    def decorator(request, *args, **kws):
        try:
            cart = models.Cart.objects.get(
                user=request.user,
                completed=False
            )
        except models.Cart.DoesNotExist:
            cart = models.Cart.objects.create(
                user=request.user
            )
        
        return function(request, cart, *args, **kws)
    
    return decorator

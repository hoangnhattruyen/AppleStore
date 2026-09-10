from .cart import Cart
from .models import PhoneModel


def cart_processor(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count': len(cart),
        'nav_phone_models': PhoneModel.objects.all()[:8],
    }

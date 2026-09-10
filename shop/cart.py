from decimal import Decimal
from django.conf import settings
from .models import ProductVariant


CART_SESSION_ID = 'apple_cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant, quantity=1, override_quantity=False):
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {
                'quantity': 0,
                'price': str(variant.price)
            }
        
        if override_quantity:
            self.cart[variant_id]['quantity'] = quantity
        else:
            self.cart[variant_id]['quantity'] += quantity

        if self.cart[variant_id]['quantity'] <= 0:
            self.remove(variant)
        else:
            self.save()

    def save(self):
        self.session.modified = True

    def remove(self, variant):
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def __iter__(self):
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product', 'phone_model', 'color')
        variant_map = {str(v.id): v for v in variants}

        for var_id, item_data in list(self.cart.items()):
            variant = variant_map.get(var_id)
            if variant:
                price = Decimal(str(item_data.get('price', variant.price)))
                qty = int(item_data.get('quantity', 1))
                total_price = price * qty
                yield {
                    'variant': variant,
                    'product': variant.product,
                    'phone_model': variant.phone_model,
                    'color': variant.color,
                    'price': price,
                    'quantity': qty,
                    'total_price': total_price,
                    'formatted_price': f"{int(price):,}đ".replace(",", "."),
                    'formatted_total_price': f"{int(total_price):,}đ".replace(",", "."),
                }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal(0)
        for item in self.cart.values():
            total += Decimal(item['price']) * item['quantity']
        return total

    @property
    def formatted_total_price(self):
        return f"{int(self.get_total_price()):,}đ".replace(",", ".")

    def get_items_json(self):
        items = []
        for item in self:
            variant = item['variant']
            items.append({
                'variant_id': variant.id,
                'product_title': variant.product.title,
                'phone_model': variant.phone_model.name,
                'color_name': variant.color.name,
                'color_hex': variant.color.hex_code,
                'image_url': f"/static/images/cases/case-{variant.color.slug}-back.png",
                'quantity': item['quantity'],
                'price': int(item['price']),
                'formatted_price': item['formatted_price'],
                'total_price': int(item['total_price']),
                'formatted_total_price': item['formatted_total_price'],
            })
        return items

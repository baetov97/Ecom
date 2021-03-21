from django import template
from ..utils import cartData

register = template.Library()

register.simple_tag()


@register.simple_tag(takes_context=True)
def get_cart_count(context):
    data = cartData(context['request'])
    cartItems = data['cartItems']
    return cartItems

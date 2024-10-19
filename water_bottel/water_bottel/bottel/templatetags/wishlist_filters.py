from django import template
from bottel.models import Wishlist  

register = template.Library()

@register.filter
def get_wishlist_item(wishlist_items, product_id):
    """Return the wishlist item for the given product_id if it exists."""
    return wishlist_items.filter(product_id=product_id).first()


    
     

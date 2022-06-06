from django import template

# from django docs - creating custom tags and filters
# loaded in template just like static eg {% load bag_tools %}
register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
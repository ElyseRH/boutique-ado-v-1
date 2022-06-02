from django.shortcuts import render
from .models import Product


def all_products(request):
    """
    Function view to return all products.
    """
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'products/products.html', context)

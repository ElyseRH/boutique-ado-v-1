from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


def all_products(request):
    """
    Function view to return all products.
    """
    products = Product.objects.all()
    # set query to None so there's no error when page is loaded without a search term
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            # searching name and description for query
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    Function view to view product_details.
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'search_term': query,
    }

    return render(request, 'products/product_detail.html', context)
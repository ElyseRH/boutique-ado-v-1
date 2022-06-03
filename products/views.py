from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    """
    Function view to return all products.
    """
    products = Product.objects.all()
    # set query to None so there's no error when page is loaded without a search term
    query = None
    categories = None
    sort = None
    direction = None  # this is for direction of sorting

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'  # to allow for lower case
                products = products.annotate(lower_name=Lower('name'))  # to allow for lower case

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'  # this adds a minus in front of the sortkey to reverse the order
            products = products.order_by(sortkey)  # this is actually sorting it


        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            # searching name and description for query
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'  # to pass the sort and dir into the html eg price asc

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
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
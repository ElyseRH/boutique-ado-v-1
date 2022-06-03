from django.shortcuts import render


def view_bag(request):
    """
    Function view to return the shopping bag contents page.
    """
    return render(request, 'bag/bag.html')

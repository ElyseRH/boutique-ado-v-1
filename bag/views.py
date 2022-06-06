
from django.shortcuts import render, redirect


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))   # will come from template as string so must convert
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})  # looks for session and initializes to empty dict if doesn't
    # now that we have dict, can put product in it

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity  # if size item already exists in same size, increment the quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity  # if size item already exists in diff size, just add to bag
        else:  # outside else block - if size item not in bag, add, as a dict
            bag[item_id] = {'items_by_size': {size: quantity}}  # dict  for size eg M: 2
    else:  # if no size, just 'quantity' code will run as below
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag # this overwrites variable with the updated version
    return redirect(redirect_url)

from django.shortcuts import render, redirect


def view_bag(request):
    """
    Function view to return the shopping bag contents page.
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):

    quantity = int(request.POST.get('quantity'))  # will come from template as string so must convert
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})  # looks for session and initializes to empty dict if doesn't
    # now that we have dict, can put product in it
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
    
    request.session['bag'] = bag  # this overwrites variable with the updated version
    print(request.session['bag'])
    return redirect(redirect_url)

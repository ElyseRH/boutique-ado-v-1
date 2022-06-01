from django.shortcuts import render

# Create your views here.

def index(request):
    """
    Function view to return the index page.
    """
    return render(request, 'home/index.html')
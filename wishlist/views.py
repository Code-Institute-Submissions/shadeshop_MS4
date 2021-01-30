from django.shortcuts import render

# Create your views here.


def view_wishlist(request):
    """ A view that renders the bag contents page """

    return render(request, 'wishlist/wishlist.html')

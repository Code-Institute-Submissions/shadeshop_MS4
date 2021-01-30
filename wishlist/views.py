from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Wishlist, WishLineItem
from profiles.models import UserProfile

# Create your views here.


@login_required
def view_wishlist(request):
    """ A view that renders the bag contents page """

    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist = profile.wishlists.all()
    
    template = 'wishlist/wishlist.html'
    context = {
        'wishlist': wishlist,
    }

    return render(request, template, context)

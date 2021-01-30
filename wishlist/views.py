from django.shortcuts import render, get_object_or_404, HttpResponse, redirect,reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Wishlist, WishLineItem
from profiles.models import UserProfile
from products.models import Product

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


def add_to_wishlist(request, product_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=product_id)
    quantity = 1 # int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist = Wishlist.objects.get(user_profile=profile)

    try:
        wishitems = WishLineItem.objects.get(product=product, wishlist=wishlist.id)
    except Exception:
        wishitems = None

    if wishitems:
        wishitems.quantity = quantity + wishitems.quantity 
        wishitems.save()
    else:
        new_wishitem = WishLineItem(
            wishlist=wishlist,
            product=product,
            quantity=quantity,
        )
        new_wishitem.save()

    return redirect(redirect_url)


def remove_from_wishlist(request, product_id):
    """Remove the item from the shopping bag"""

    try:
        wish = get_object_or_404(WishLineItem, product=product_id)
        wish.delete()
        messages.success(request, f'Removed {wish.product.name} from your wishlist!')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}.')
        return HttpResponse(status=500)


def adjust_wishlist(request, product_id):
    """Adjust the quantity of the specified product to the specified amount"""

    wish = get_object_or_404(WishLineItem, product=product_id)
    quantity = int(request.POST.get('quantity'))

    if quantity > 0:
        wish.quantity = quantity
        wish.save()
        messages.success(request, f'Updated {wish.product.name} quantity!')
    else:
        wish.delete()
        messages.success(request, f'Removed {wish.product.name} from your wishlist!')

    return redirect(reverse('view_wishlist'))

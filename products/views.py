from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Brand


# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    brands = Brand.objects.all()
    query = None
    gender = None
    brand = None
    sale = None

    if request.GET:
        if 'sale' in request.GET:
            sale = request.GET['sale']
            if 'gender' in request.GET:
                gender = request.GET['gender']
                queries = Q(gender__in=gender) & Q(sale=sale)
                products = products.filter(queries)
            else:
                products = products.filter(sale=sale)
        else:
            if 'gender' in request.GET:
                gender = request.GET['gender']
                if 'brand' in request.GET:
                    brand = request.GET['brand']
                    queries = Q(gender__in=gender) & Q(brand__in=brand)
                    products = products.filter(queries)
                    brand = brands.filter(id=brand)
                else:
                    products = products.filter(gender__in=gender)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'brand': brand,
        'gender': gender,
        'sale': sale,
    }

    print(context)

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

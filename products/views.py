from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Brand, Review
from .forms import ProductForm, ReviewForm
from profiles.models import UserProfile
from checkout.models import Order, OrderLineItem

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    brands = Brand.objects.all()
    query = None
    gender = None
    brand = None
    sale = None
    sort = None
    direction = None

    if request.GET:
        # Return Products by Sort Request
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'brand':
                sortkey = 'brand__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        # Return Products based on selection through navbar
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
        # return products based on user search input
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'brand': brand,
        'gender': gender,
        'sale': sale,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail"""

    product = get_object_or_404(Product, pk=product_id)
    orderitems = OrderLineItem.objects.all().filter(product=product)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        all_orders = Order.objects.filter(user_profile=profile)
        queries = Q(order__in=all_orders) & Q(product=product)
        user_orders = orderitems.filter(queries)
    else:
        user_orders = None

    review_form = ReviewForm()

    context = {
        'product': product,
        'user_orders': user_orders,
        'review_form': review_form,
    }

    print(context)

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.info(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to add product.'
                'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product.'
                'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.info(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)

        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user_profile = user_profile
            new_review.product = product
            new_review.save()
            messages.info(request, 'Successfully added product review!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to add review.'
                'Please ensure the form is valid.')


@login_required
def delete_review(request, review_id):
    """ Delete a product from the store """
    review = get_object_or_404(Review, pk=review_id)
    product = review.product
    review.delete()
    messages.info(request, 'Review deleted!')
    return redirect(reverse('product_detail', args=[product.id]))

from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def home(request):
    products_all = []
    category_types = Product.objects.values('category').distinct()
    categories = [c['category'] for c in category_types]

    for category in categories:
        product = Product.objects.filter(category=category)
        products_all.append(product)

    params = {'products_all':products_all}

    return render(request, 'shop/index.html', params)

def about(request):
    return HttpResponse("About Page")

def contact(request):
    return HttpResponse("Contact Page")

def tracker(request):
    return HttpResponse("Tracker Page")

def search(request):
    return HttpResponse("Search Page")

def view_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    params = {'product':product}

    return render(request, 'shop/view-product.html', params)

def view_cart(request):
    return render(request, 'shop/view-cart.html')

def checkout(request):
    return HttpResponse("Checkout Page")

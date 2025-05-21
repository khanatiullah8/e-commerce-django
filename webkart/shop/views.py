from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact

# home
def home(request):
    products_all = []
    category_types = Product.objects.values('category').distinct()
    categories = [c['category'] for c in category_types]

    for category in categories:
        product = Product.objects.filter(category=category)
        products_all.append(product)

    params = {'products_all':products_all}

    return render(request, 'shop/index.html', params)

# about us
def about(request):
    return render(request, 'shop/about.html')

# contact us
def contact(request):
    is_form_submitted = "no"
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        is_form_submitted = "yes"
    else:
        is_form_submitted = "no"

    return render(request, 'shop/contact.html', {'is_form_submitted':is_form_submitted})

def tracker(request):
    return HttpResponse("Tracker Page")

def search(request):
    return HttpResponse("Search Page")

# product view
def view_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    params = {'product':product}

    return render(request, 'shop/view-product.html', params)

# cart view
def view_cart(request):
    return render(request, 'shop/view-cart.html')

# checkout
def checkout(request):
    return HttpResponse("Checkout Page")

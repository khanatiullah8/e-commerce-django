from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order, Product, Contact

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
    thank = "false"
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        desc = request.POST.get("desc", "")

        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = "true"

    return render(request, 'shop/contact.html', {'thank':thank})

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
def view_checkout(request):
    thank = 'false'
    id = ''
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        address2 = request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip", "")
        phone = request.POST.get("phone", "")

        order = Order(items_json=items_json, name=name, email=email, address=address, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank = 'true'
        id = order.id

    return render(request, 'shop/view-checkout.html', {'thank':thank, 'id':id})

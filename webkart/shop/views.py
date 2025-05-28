import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import razorpay.errors
from .models import Order, Product, Contact, OrderUpdate
import razorpay
from django.conf import settings
from .forms import ContactForm

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
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form.send_mail()
            thank = "true"
    else:
        form = ContactForm()

    context = {"form": form, "thank": thank}
    return render(request, "shop/contact.html", context)

# tracker
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get("email", "")
        try:
            order = Order.objects.filter(id=orderId, email=email).first()
            if order:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for i in update:
                    updates.append({'text': i.update_desc, 'date': i.timestamp})
                return HttpResponse(json.dumps({'updates':updates,'orderDetails':order.items_json}, default=str))
            else:
                return HttpResponse(json.dumps({'updates':[],'orderDetails':'[]'}))
        except Exception as e:
            return HttpResponse("error")
    return render(request, 'shop/tracker.html')

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


# ========= Payment Integration - start =============

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# create order
def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = data.get("amount")
        currency = data.get("currency")
        
        order_data = {
            "amount": amount,
            "currency": currency,
            "payment_capture": "1",
        }

        razorpay_order = razorpay_client.order.create(data=order_data)

        params = {
            "order_id": razorpay_order.get("id"),
            "amount": amount,
            "currency": currency,
            "razorpay_merchant_key": settings.RAZORPAY_KEY_ID
        }
        return JsonResponse(params)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# verify signature
def verify_signature(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_id = data.get("razorpay_payment_id")
        order_id = data.get("razorpay_order_id")
        signature = data.get("razorpay_signature")
        
        try: 
            razorpay_client.utility.verify_payment_signature({
                "razorpay_payment_id": payment_id,
                "razorpay_order_id": order_id,
                "razorpay_signature": signature
            })
            return JsonResponse({"payment_success": "true"})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "signature verification failed"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# save all checkout products in database
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
        orderUpdate = OrderUpdate(order_id=order.id, update_desc='The order has been placed')
        orderUpdate.save()
        thank = 'true'
        id = order.id

    return render(request, 'shop/view-checkout.html', {'thank': thank, 'id': id})

# ========= Payment Integration - end =============

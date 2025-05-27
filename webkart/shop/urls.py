from django.urls import path
from . import views 

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('viewproduct/<int:product_id>/', views.view_product, name='viewproduct'),
    path('viewcart/', views.view_cart, name='viewcart'),
    path('viewcheckout/', views.view_checkout, name='viewcheckout'),
    path('order/', views.create_order, name='order'),
    path('verify/', views.verify_signature, name='verify'),
    path('tracker/', views.tracker, name='tracker'),
    path('search/', views.search, name='search'),
]
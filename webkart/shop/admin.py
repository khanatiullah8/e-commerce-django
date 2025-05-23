from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Contact, Order, OrderUpdate

# Register your models here.
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductAdmin(ImportExportModelAdmin):
    resource_classes = [ProductResource]

admin.site.register(Product, ProductAdmin)

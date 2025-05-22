from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    desc = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="shop/images/", default="")

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    desc = models.TextField()

    def __str__(self):
        return self.name
    
class Order(models.Model):
    items_json = models.TextField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.email
    
class OrderUpdate(models.Model):
    order_id = models.IntegerField()
    update_desc = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.update_desc if len(self.update_desc) < 20 else self.update_desc[:20] + "..."
    
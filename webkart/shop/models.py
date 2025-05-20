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
    
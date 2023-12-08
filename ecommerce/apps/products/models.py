from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)

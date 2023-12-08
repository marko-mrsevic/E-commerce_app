from django.db import models
from ..products.models import Product
from ..users.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    is_purchased = models.BooleanField(default=False)

    def total_price(self):
        items = self.items.all()
        amount = 0
        for item in items:
            amount += item.quantity * item.product.price
        return amount


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')

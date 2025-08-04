from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_desc = models.TextField()
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_stock = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    invoice_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_paid = models.BooleanField(default=False)

    def get_total_cost(self):
        return sum(item.quantity * item.price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    price = models.DecimalField(max_digits=8, decimal_places=2)

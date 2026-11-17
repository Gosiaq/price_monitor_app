# products/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10)
    shop = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    multipack = models.CharField(max_length=50, default='1 x')
    quantity = models.CharField(max_length=100, null=True, blank=True)
    unit_measure = models.CharField(max_length=10, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    url = models.URLField(max_length=1000, unique=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
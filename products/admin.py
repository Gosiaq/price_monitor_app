from django.contrib import admin
from .models import Product, PriceHistory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'multipack', 'quantity', 'price', 'currency', 'unit_price', 'shop', 'category', 'timestamp')
    list_filter = ('shop', 'category')
    search_fields = ('name',)

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'timestamp')
    list_filter = ('timestamp', 'product')
    search_fields = ('product__name',)
    readonly_fields = ('timestamp',)
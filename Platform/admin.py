from django.contrib import admin
from .models import Product

# # Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_stock', 'created_at')
    search_fields = ('product_name',)
    list_filter = ('created_at',)

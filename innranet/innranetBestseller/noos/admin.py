from django.contrib import admin
from .models import Product, colorVariant, Variant, Store, Inventory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'itemNo')  # Fields to display in the list view
    search_fields = ('name', 'ItemNo')              # Fields to search

@admin.register(colorVariant)
class ColorVariantsAdmin(admin.ModelAdmin):
    list_display = ('product', 'colorName', 'colorCode', 'noos')  # Display product relationship and color details
    search_fields = ('colorName', 'colorCode')
    list_filter = ('colorName',)
    list_filter = ('noos',)                         # Filter options

@admin.register(Variant)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ('colorVariant', 'BarcodeNo', 'size', 'length')  # Display variant details
    search_fields = ('BarcodeNo', 'size', 'length')
    list_filter = ('size', 'length')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_name')  # Display store information
    search_fields = ('store_name',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'variant', 'quantity')  # Display inventory details
    search_fields = ('store__store_name', 'variant__BarcodeNo')  # Enable search for related fields
    list_filter = ('store',)
    autocomplete_fields = ('store', 'variant')  # Improves usability for large datasets
    
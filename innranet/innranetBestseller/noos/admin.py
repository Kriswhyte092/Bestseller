from django.contrib import admin
from .models import Product, Store, Inventory
from django.db import models  # Add this import

# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory Level'
    parameter_name = 'inventory_level'

    def lookups(self, request, model_admin):
        return [
            ('zero_or_below', 'Zero or Below'),
            ('above_zero', 'Above Zero'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'zero_or_below':
            return queryset.filter(inventory__quantity__lte=0)
        elif self.value() == 'above_zero':
            return queryset.filter(inventory__quantity__gt=0)

# Custom filter for has_image_urls# Custom filter for has_image_urls
class HasImageUrlsFilter(admin.SimpleListFilter):
    title = 'Has Image URLs'  # Display title in the admin
    parameter_name = 'has_image_urls'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Has Image URLs'),
            ('no', 'No Image URLs'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image_urls=[])
        elif self.value() == 'no':
            return queryset.filter(image_urls=[])
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('ItemNo', 'VariantCode', 'BarcodeNo', 'VariantName', 'noos', 'has_image_urls', 'inventory_level')
    list_filter = ('noos', HasImageUrlsFilter)
    search_fields = ('ItemNo', 'VariantCode', 'BarcodeNo', 'VariantName')  # Fields to search in

    def has_image_urls(self, obj):
        return bool(obj.image_urls)
    has_image_urls.boolean = True
    has_image_urls.short_description = 'Has Image URLs'

    def inventory_level(self, obj):
        # Aggregate total inventory across all stores for this product
        inventory = obj.inventory_set.aggregate(total=models.Sum('quantity'))['total']
        return inventory if inventory else 0
    inventory_level.short_description = 'Total Inventory'


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 0  # Prevent extra empty rows
    fields = ('product', 'quantity', 'noos_status', 'has_image_urls_status')
    readonly_fields = ('product', 'quantity', 'noos_status', 'has_image_urls_status')  # Make fields read-only

    def noos_status(self, obj):
        # Access the related product's noos field
        return obj.product.noos
    noos_status.short_description = 'Noos'
    noos_status.boolean = True  # Show checkmarks in the admin

    def has_image_urls_status(self, obj):
        # Check if the related product has image URLs
        return bool(obj.product.image_urls)
    has_image_urls_status.short_description = 'Has Image URLs'
    has_image_urls_status.boolean = True  # Show checkmarks in the admin


class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name',)  # Adjust fields as per your Store model
    inlines = [InventoryInline]  # Include the inline for inventory

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'quantity', 'has_image_urls')
    list_filter = ('store', 'product')
    

admin.site.register(Store, StoreAdmin)
admin.site.register(Inventory)
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

    def has_image_urls(self, obj):
        return bool(obj.image_urls)
    has_image_urls.boolean = True
    has_image_urls.short_description = 'Has Image URLs'

    def inventory_level(self, obj):
        # Aggregate total inventory across all stores for this product
        inventory = obj.inventory_set.aggregate(total=models.Sum('quantity'))['total']
        return inventory if inventory else 0
    inventory_level.short_description = 'Total Inventory'


admin.site.register(Store)

admin.site.register(Inventory)
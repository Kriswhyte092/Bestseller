from django.contrib import admin
from .models import Product, colorVariant, Variant, Store, Inventory
from django.db import models


class InventoryLevelFilter(admin.SimpleListFilter):
    title = ('Inventory Level')
    parameter_name = 'inventory_level'

    def lookups(self, request, model_admin):
        return (
            ('below_0', ('Below 0')),
            ('low', ('Low')),
            ('medium', ('Medium')),
            ('high', ('High')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'below_0':
            return queryset.filter(quantity__lt=0)
        if self.value() == 'low':
            return queryset.filter(quantity__lt=10)
        if self.value() == 'medium':
            return queryset.filter(quantity__gte=10, quantity__lt=50)
        if self.value() == 'high':
            return queryset.filter(quantity__gte=50)
        return queryset

class HasImageURLsFilter(admin.SimpleListFilter):
    title = ('Has Image URLs')
    parameter_name = 'has_image_urls'

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Yes')),
            ('no', ('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(image_urls__isnull=False).exclude(image_urls=[])
        if self.value() == 'no':
            return queryset.filter(image_urls__isnull=True) | queryset.filter(image_urls=[])
        return queryset

class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 0  # No extra empty forms
    fields = ('variant', 'quantity', 'noos_status', 'has_image_urls_status')  # Fields to display
    readonly_fields = ('variant', 'quantity', 'noos_status', 'has_image_urls_status')  # Make fields read-only

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

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0  # No extra empty forms
    fields = ('BarcodeNo', 'size', 'length')  # Fields to display
    readonly_fields = ('BarcodeNo', 'size', 'length')  # Make fields read-only

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'itemNo')  # Fields to display in the list view
    search_fields = ('name', 'itemNo')              # Fields to search

@admin.register(colorVariant)
class ColorVariantsAdmin(admin.ModelAdmin):
    list_display = ('product', 'colorName', 'colorCode', 'noos', 'has_image_urls_status')  # Display product relationship and color details
    search_fields = ('colorName', 'colorCode')
    list_filter = ('noos', HasImageURLsFilter)                         # Filter options
    inlines = [VariantInline]  # Add the inline admin class
    
    def has_image_urls_status(self, obj):
        # Check if the related product has image URLs
        return bool(obj.image_urls)
    has_image_urls_status.short_description = 'Has Image URLs'
    has_image_urls_status.boolean = True  # Show checkmarks in the admin

@admin.register(Variant)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ('colorVariant', 'BarcodeNo', 'size', 'length')  # Display variant details
    search_fields = ('BarcodeNo', 'size', 'length')
    list_filter = ('size', 'length', )  # Add custom filter
    inlines = [InventoryInline]  # Add the inline admin class

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_name')  # Display store information
    search_fields = ('store_name',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'variant', 'variant_size', 'quantity')
    search_fields = ('store__store_name', 'variant__BarcodeNo')
    list_filter = ('store', InventoryLevelFilter)
    autocomplete_fields = ('store', 'variant')

    fields = (
        'store_name_display',
        'variant_barcode_display',
        'variant_color_display',
        'variant_size_display',
        'variant_length_display',
        'quantity'
    )
    readonly_fields = (
        'store_name_display',
        'variant_barcode_display',
        'variant_color_display',
        'variant_size_display',
        'variant_length_display'
    )

    def store_name_display(self, obj):
        return obj.store.store_name if obj.store else ''
    store_name_display.short_description = 'Store Name'

    def variant_barcode_display(self, obj):
        return obj.variant.BarcodeNo if obj.variant else ''
    variant_barcode_display.short_description = 'Barcode'

    def variant_color_display(self, obj):
        return obj.variant.colorVariant.colorName if obj.variant and obj.variant.colorVariant else ''
    variant_color_display.short_description = 'Color Name'

    def variant_size_display(self, obj):
        return obj.variant.size if obj.variant else ''
    variant_size_display.short_description = 'Size'

    def variant_length_display(self, obj):
        return obj.variant.length if obj.variant else ''
    variant_length_display.short_description = 'Length'
    
# 5713748311462
# 5715516200558
# 5715607268436
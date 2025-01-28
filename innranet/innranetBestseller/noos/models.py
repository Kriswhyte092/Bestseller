from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    itemNo = models.CharField(max_length=255)
    product_description = models.TextField(default="No description added")
    
    def get_variant(self, variant_code):
        # Filter variants directly by the BarcodeNo within the related color variants
        variant = Variant.objects.filter(colorVariant__product=self, BarcodeNo=variant_code).first()
        if not variant:
            return None  # Explicitly return None for clarity
        return variant

    def __str__(self):
        color_variants_info = [
            f"{color_variant.colorName} ({color_variant.variants.count()} variants)"
            for color_variant in self.color_variants.all()
        ]

        color_variants_str = "\n".join(color_variants_info)

        return (
            f"{self.name} ({self.itemNo})"
            f" - {len(self.color_variants.all())} color variants\n"
            # f"{color_variants_str}"
        )
        
class colorVariant(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="color_variants"
    )
    colorName = models.CharField(max_length=255)
    colorCode = models.CharField(max_length=50)
    noos = models.BooleanField(default=False)
    # Variants will be referenced by a reverse relationship.
    # image_urls can be handled by a separate model or a JSON field:
    image_urls = models.JSONField(default=list)  # if you're on Django 3.1+

    def __str__(self):
        return f"{self.product.name} / {self.colorName}"

class Variant(models.Model):
    colorVariant = models.ForeignKey(
        colorVariant, 
        on_delete=models.CASCADE, 
        related_name="variants"
    )
    BarcodeNo = models.BigIntegerField(default=0)
    size = models.CharField(max_length=50)
    length = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.colorVariant.product.name} / {self.colorVariant.colorName} - [Barcode: {self.BarcodeNo}] "

class Store(models.Model):
    store_name = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name

class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
            unique_together = ('store', 'variant')  # Ensures one inventory record per store-product pair

    def __str__(self):
        return f"{self.store} / {self.variant} / Qty: {self.quantity}"

    def variant_size(self):
        return self.variant.size
    variant_size.short_description = 'Variant Size'
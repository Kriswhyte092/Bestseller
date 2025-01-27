from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    ItemNo = models.CharField(max_length=255)
    colorVariants = models.JSONField(default=list, blank=True)
    noos = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ItemNo} - {self.VariantCode} - {self.BarcodeNo} - {self.VariantName}"  # Adjust as necessary

class colorVariant(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="color_variants"
    )
    colorName = models.CharField(max_length=255)
    colorCode = models.CharField(max_length=255)
    variant_details = models.JSONField(default=list, blank=True)
    image_urls = models.JSONField(blank=True, default=list)  # Updated to use callable default

    def __str__(self):
        return f"{self.colorCode} - {self.colorName}"

class Variant(models.Model):
    colorVariant = models.ForeignKey(
        colorVariant,
        on_delete=models.CASCADE,
        related_name="related_variants"  # Avoids clash
    )
    BarcodeNo = models.IntegerField(("BarcodeNo"), blank=True, null=True)
    size = models.CharField(max_length=255)
    length = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.VariantCode} - {self.BarcodeNo}"

class Store(models.Model):
    store_name = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name

class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, default=None) 
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('store', 'variant')  # Ensures one inventory record per store-product pair

    def __str__(self):
        return f"{self.store.store_name} - {self.variant.VariantCode} - {self.quantity}"

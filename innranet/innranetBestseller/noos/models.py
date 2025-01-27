from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    itemNo = models.CharField(max_length=255)
    product_description = models.TextField(default="No description added")

    def __str__(self):
        return f"{self.name} ({self.itemNo})"

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
        return f"[{self.BarcodeNo}] {self.colorVariant.colorName}"

class Store(models.Model):
    store_name = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name

class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.store} / {self.variant} / Qty: {self.quantity}"

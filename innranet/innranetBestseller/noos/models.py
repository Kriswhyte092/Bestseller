from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Product(models.Model):
    ItemNo = models.CharField(max_length=255)
    VariantCode = models.CharField(max_length=255)
    VariantName = models.CharField(max_length=255)
    BarcodeNo = models.CharField(max_length=255, default="")
    image_urls = models.JSONField(blank=True, default=list)
    noos = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ItemNo} - {self.VariantCode} - {self.BarcodeNo} - {self.VariantName}"  # Adjust as necessary


class Store(models.Model):
    store_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.store_name


class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('store', 'product')  # Ensures one inventory record per store-product pair

    def __str__(self):
        return f"{self.product.ItemNo} / {self.product.VariantCode} - {self.store.store_name}: {self.quantity} units"

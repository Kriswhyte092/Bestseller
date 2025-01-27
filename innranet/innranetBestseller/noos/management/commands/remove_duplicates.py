from django.core.management.base import BaseCommand
from noos.models import Product, colorVariant, Variant, Store, Inventory
from django.db.models import Count

class Command(BaseCommand):
    help = "Remove duplicate products, colorVariants, Variants, Stores, and Inventory from the database"

    def handle(self, *args, **kwargs):
        self.remove_duplicates(Product, ['name', 'itemNo'], "products")
        self.remove_duplicates(colorVariant, ['product', 'colorName', 'colorCode'], "colorVariants")
        self.remove_duplicates(Variant, ['colorVariant', 'BarcodeNo', 'size'], "Variants")
        self.remove_duplicates(Store, ['store_name'], "Stores")
        self.remove_duplicates(Inventory, ['store', 'variant'], "Inventory")

    def remove_duplicates(self, model, fields, model_name):
        duplicates = (
            model.objects.values(*fields)
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )
        number_of_duplicates = len(duplicates)
        
        if not duplicates:
            self.stdout.write(self.style.SUCCESS(f"No duplicate {model_name} found!"))
            return

        for duplicate in duplicates:
            items = model.objects.filter(**{field: duplicate[field] for field in fields})
            items.exclude(id=items.first().id).delete()

        self.stdout.write(self.style.NOTICE(f"Successfully removed {number_of_duplicates} duplicate {model_name}!"))

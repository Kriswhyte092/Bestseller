from django.core.management.base import BaseCommand
from noos.models import Product
from django.db.models import Count

class Command(BaseCommand):
    help = "Remove duplicate products from the database"

    def handle(self, *args, **kwargs):
        count = Product.objects.count()
        if count == 0:
            self.stdout.write(self.style.WARNING("No products found in the database!"))
            return
                
        duplicates = (
            Product.objects.values('name', 'itemNo')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )
        number_of_duplicates = len(duplicates)
        
        if not duplicates:
            self.stdout.write(self.style.SUCCESS("No duplicate products found!"))
            return

        for duplicate in duplicates:
            products = Product.objects.filter(name=duplicate['name'], itemNo=duplicate['itemNo'])
            products.exclude(id=products.first().id).delete()

        self.stdout.write(self.style.SUCCESS(f"Successfully removed {number_of_duplicates} duplicate products!"))

from django.core.management.base import BaseCommand
from noos.models import Product
from tqdm import tqdm 

class Command(BaseCommand):
    help = "Delete all products from the database"

    def handle(self, *args, **kwargs):
        # Confirm action with the user
        confirm = input("Are you sure you want to delete all products? Type 'yes' to confirm: ").lower()
        if confirm == 'yes':
            products = Product.objects.all()
            total_products = products.count()

            if total_products == 0:
                self.stdout.write(self.style.WARNING("No products found to delete."))
                return

            self.stdout.write(f"Deleting {total_products} products...")
            
            # Use tqdm to display the progress bar
            for product in tqdm(products, desc="Deleting Products", unit="product"):
                product.delete()

            self.stdout.write(self.style.SUCCESS(f"Successfully deleted {total_products} products!"))
        else:
            self.stdout.write(self.style.WARNING("Aborted. No products were deleted."))
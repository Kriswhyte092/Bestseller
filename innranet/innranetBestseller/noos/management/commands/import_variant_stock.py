import json
from django.core.management.base import BaseCommand
from django.db import transaction
from noos.models import Product, Inventory, Store  
from noos.import_products import import_product  
from noos.product_apis import fashion_cloud_api
from tqdm import tqdm 
import logging
import time
import atexit

logging.basicConfig(
        filename="log/import_variant_stock_errors.log",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

class Command(BaseCommand):
    help = "Process variant stock and update product inventory"
    
# Define the exit handler
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        atexit.register(self.on_exit)

    def on_exit(self):
        elapsed_time = time.time() - self.start_time
        logging.info(f"Processing completed in {elapsed_time:.2f} seconds or {elapsed_time/60:.2f} minutes")
        self.stdout.write(f"Processing completed in {elapsed_time:.2f} seconds or {elapsed_time/60:.2f} minutes")

    def handle(self, *args, **kwargs):
        file_path = "variant_stock.json"  # Hardcoded file path
        
        try:
            variant_stock_data = self.load_json(file_path)
            self.process_variant_stock(variant_stock_data)
            self.stdout.write(self.style.SUCCESS("Processing completed!"))
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            self.stdout.write(self.style.ERROR("Processing failed. Check logs for details."))

    def load_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def process_variant_stock(self, data):
        
        with transaction.atomic():
            for record in tqdm(data["value"], desc="Processing records", leave=True, colour="green", position=0):
                try:
                    item_no = record["ItemNo"]
                    variant_code = record.get("barcodeNo", "").strip()
                    if not variant_code:
                        logging.warning(f"Missing barcodeNo for ItemNo {item_no}. Skipping record.")
                        self.stdout.write(self.style.WARNING(f"Missing barcodeNo for ItemNo {item_no}. Skipping record."))
                        continue
                    location_code = record["LocationCode"]
                    inventory_count = record["Inventory"]

                    product = Product.objects.filter(itemNo=item_no).first()
                    self.stdout.write(f"Product: {product}")
                    if not product:
                        fashion_cloud_product = fashion_cloud_api(item_no)
                        if not fashion_cloud_product:
                            logging.error(f"API returned no data for ItemNo {item_no}")
                            self.stdout.write(self.style.ERROR(f"API returned no data for ItemNo {item_no}"))
                            continue 
                        
                        product, v = import_product(fashion_cloud_product, item_no)
                        self.stdout.write(f"New Product: {product}")
                        if not product:
                            logging.error(f"Product {item_no} could not be created.")
                            self.stdout.write(self.style.ERROR(f"Product {item_no} could not be created."))
                            continue
                        else:
                            self.stdout.write(self.style.NOTICE(f"New Product created - {item_no} / {product.name}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Product {item_no} already exists"))

                    # Check if the store exists, create if not
                    store, created = Store.objects.get_or_create(
                        store_name=location_code,
                        defaults={"store_name": location_code}  # Provide a default name for new stores
                    )
                    store.save()
                    self.stdout.write(f"Store: {store}, New: {created}")

                    # Link variant and inventory
                    variant = product.get_variant(variant_code)
                    self.stdout.write(f"-- Variant: {variant}")
                    if not variant:
                        logging.error(f"Variant {variant_code} for Product {item_no} does not exist.")
                        self.stdout.write(self.style.ERROR(f"Variant did not exist - {variant_code}"))
                        continue

                    # Update or create inventory
                    inventory, created = Inventory.objects.get_or_create(
                        store=store,
                        variant=variant,
                        defaults={"quantity": inventory_count}
                    )
                    self.stdout.write(f"Inventory: {inventory}, Created: {created}")
                    if not created:
                        self.stdout.write(self.style.SUCCESS(f"Inventory exists and updated - {store} / {variant.colorVariant.colorName} {inventory}"))
                        inventory.quantity = inventory_count

                    inventory.save()
                    
                    self.stdout.write()
                except Exception as e:
                    logging.error(f"Error processing record {record}: {e}")
                    self.stdout.write(self.style.ERROR(f"Error processing record {record}: {e}"))
                    self.stdout.write()

        elapsed_time = time.time() - self.start_time
        self.stdout.write(self.style.SUCCESS(f"Processing completed in {elapsed_time:.2f} seconds or {elapsed_time/60:.2f} minutes - {len(data)} records processed"))

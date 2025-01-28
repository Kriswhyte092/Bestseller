import json
import logging
import time
import atexit

from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from noos.models import Product, Inventory, Store
from noos.import_products import import_product
from noos.product_apis import fashion_cloud_api

# Configure logging
logging.basicConfig(
    filename="log/import_variant_stock_log.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Command(BaseCommand):
    """
    Management command to import variant stock data from a JSON file
    and update the product inventory in the database.
    """
    help = "Process variant stock and update product inventory"

    def __init__(self):
        """
        Initialize the command, store the start time, and register an exit
        handler to log the total processing time.
        """
        super().__init__()
        self.start_time = time.time()
        atexit.register(self.on_exit)

    def on_exit(self):
        """
        Callback function executed on program exit. Logs the total time
        spent processing and displays it in the Django console as an error.
        """
        elapsed_time = time.time() - self.start_time
        logging.info(f"Processing completed in {elapsed_time:.2f} seconds "
                     f"or {elapsed_time/60:.2f} minutes")
        self.stdout.write(
            self.style.ERROR(
                f"Processing exited after {elapsed_time:.2f} seconds "
                f"or {elapsed_time/60:.2f} minutes"
            )
        )

    def handle(self, *args, **kwargs):
        """
        Main entry point for the management command. Attempts to load JSON
        data from a file and process it to update product inventory.
        """
        file_path = "variant_stock.json"  # Hardcoded file path
        
        try:
            # Load the JSON data.
            variant_stock_data = self.load_json(file_path)

            # Process the stock data.
            self.process_variant_stock(variant_stock_data)

            logging.info("Processing completed!")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            self.stdout.write(
                self.style.ERROR("Processing failed. Check logs for details.")
            )

    def load_json(self, file_path):
        """
        Load JSON data from the provided file path.

        :param file_path: The path to the JSON file containing variant stock data.
        :return: Parsed JSON data as a Python dictionary.
        """
        with open(file_path, 'r') as file:
            return json.load(file)

    def process_variant_stock(self, data):
        """
        Iterate over each record in the JSON data and process it
        within a database transaction.
        """
        count=0
        with transaction.atomic():
            for record in tqdm(
                data["value"],
                desc="Processing records",
                unit="variant",
                ascii="_#",
                colour="blue"
            ):
                count+=1
                if count==10000:
                    break
                try:
                    self.handle_variant_record(record)
                except Exception as e:
                    logging.error(f"Error processing record {record}: {e}")
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error processing record {record}: {e}"
                        )
                    )

        # Calculate total processing time at the end of the function.
        elapsed_time = time.time() - self.start_time
        logging.info(
            f"Processing completed in {elapsed_time:.2f} seconds or "
            f"{elapsed_time/60:.2f} minutes - {len(data)} records processed"
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Processing completed in {elapsed_time:.2f} seconds or "
                f"{elapsed_time/60:.2f} minutes - {len(data['value'])} records processed"
            )
        )

    def handle_variant_record(self, record):
        """
        Handle the logic for a single variant record, including:

        1. Extracting the relevant fields (ItemNo, barcodeNo, etc.).
        2. Fetching or creating the product.
        3. Fetching or creating the store.
        4. Fetching the variant by barcode.
        5. Creating or updating the Inventory record.

        :param record: A single record from the JSON data.
        """
        item_no = record["ItemNo"]
        variant_code = record.get("barcodeNo", "").strip()
        location_code = record["LocationCode"]
        inventory_count = record["Inventory"]

        # Skip if variant_code is missing.
        if not variant_code:
            logging.warning(
                f"Missing barcodeNo for ItemNo {item_no} store: {location_code}. Skipping record."
            )
            return
        
        product = self.get_or_create_product(item_no, variant_code, location_code, inventory_count)
        if not product:
            # Could not fetch or create the product, so skip this record.
            return

        store = self.get_or_create_store(location_code)

        variant = self.get_variant(product, variant_code, item_no)
        if not variant:
            # Could not find the variant, so skip this record.
            return

        # Finally, update or create the inventory.
        self.create_or_update_inventory(store, variant, inventory_count)

    def get_or_create_product(self, item_no, variant_code, location_code, inventory_count):
        """
        Fetch a Product by ItemNo. If it doesn't exist, attempt to fetch
        data from the Fashion Cloud API and create one.

        :param item_no: The unique item number (product code).
        :return: A Product instance or None if not found or creation failed.
        """
        product = Product.objects.filter(itemNo=item_no).first()
        if product:
            logging.info(f"Product {item_no} already exists.")
            return product
        
        # If the product does not exist, call the API and import.
        fashion_cloud_product = fashion_cloud_api(item_no)
        if not fashion_cloud_product:
            logging.error(f"API returned no data for ItemNo {item_no}")
            self.stdout.write(
                self.style.ERROR(f"API returned no data for ItemNo {item_no}")
            )
            return None
        
        product, status = import_product(fashion_cloud_product, item_no)
        if not product:
            logging.error(f"Could not created product: {item_no} for variant: {variant_code} - store {location_code} {inventory_count}")
            return None
        
        logging.info(f"New Product created - {item_no} / {product.name}")
        return product

    def get_or_create_store(self, location_code):
        """
        Fetch or create a Store by location_code.

        :param location_code: String representing the store's location code.
        :return: A Store instance.
        """
        store, created = Store.objects.get_or_create(
            store_name=location_code,
            defaults={"store_name": location_code}  # Provide any additional defaults here
        )
        if created:
            logging.info(f"Store {store} created.")
        else:
            logging.info(f"Store {store} already exists.")
        
        return store

    def get_variant(self, product, variant_code, item_no):
        """
        Fetch a variant from a Product using the barcode (variant_code).

        :param product: A Product instance.
        :param variant_code: The barcode for the variant.
        :param item_no: The product's item number, for logging.
        :return: The variant object or None if it doesn't exist.
        """
        variant = product.get_variant(variant_code)
        if not variant:
            logging.error(
                f"Variant {variant_code} for Product {item_no} does not exist."
            )
            self.stdout.write(
                self.style.ERROR(
                    f"Variant {variant_code} for Product {item_no} does not exist."
                )
            )
            return None
        
        logging.info(f"Variant {variant_code} found for Product {item_no}.")
        return variant

    def create_or_update_inventory(self, store, variant, inventory_count):
        """
        Fetch or create an Inventory record, and update its quantity.

        :param store: A Store instance.
        :param variant: A Product variant instance.
        :param inventory_count: The current inventory count for this variant/store.
        :return: The Inventory object (created or updated).
        """
        inventory, created = Inventory.objects.get_or_create(
            store=store,
            variant=variant,
            defaults={"quantity": inventory_count}
        )
        if created:
            logging.info(
                f"New Inventory created for store {store.store_name} "
                f"and variant {variant} with quantity {inventory_count}."
            )
        else:
            inventory.quantity = inventory_count
            inventory.save()
            logging.info(
                f"Inventory updated for store {store.store_name} "
                f"and variant {variant} to quantity {inventory_count}."
            )
        
        return inventory

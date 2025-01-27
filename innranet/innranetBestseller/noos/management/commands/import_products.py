from django.core.management.base import BaseCommand
from noos.import_products import import_product, JJ_noos_barcodes
from noos.product_apis import fashion_cloud_api
from tqdm import tqdm
import logging

logging.basicConfig(filename='log/import_products.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s:%(message)s')

class Command(BaseCommand):
    help = 'Import products from Fashion Cloud API'

    def handle(self, *args, **kwargs):
        for code in tqdm(JJ_noos_barcodes, desc="Processing products"):
            try:
                fashion_cloud_product = fashion_cloud_api(code)
                if fashion_cloud_product is None:
                    logging.error(f"Error fetching data for barcode: {code}")
                    self.stdout.write(self.style.ERROR(f"Error fetching data for barcode: {code}"))
                    continue
                p, v = import_product(fashion_cloud_product, code)
                #self.stdout.write(self.style.SUCCESS(f'Successfully imported product: {p.name}'))
            except Exception as e:
                logging.error(f"Error processing barcode {code}: {e}")
                self.stdout.write(self.style.ERROR(f"Error processing barcode {code}: {e}"))
                continue
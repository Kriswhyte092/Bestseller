"""Kóði sem les inn JSON skrá og vistar gögn í gagnagrunn"""

import json
from noos.models import Product, Store, Inventory  # Replace `myapp` with your app name

# Load JSON data
with open('variant_stock.json') as f:
    data = json.load(f)["value"]

# Store location mapping
store_mapping = {
        "VMK": "Vero Moda Kringlan",
        "VIK": "Vila Kringla",
        "NIK": "Name It Kringlan",
        "JJK": "Jack & Jones Kringlan",
        "SLK": "Selected Kringlan",
        "VMS": "Vero Moda Smáralind",
        "VIS": "Vila Smáralind",
        "NIS": "Name It Smáralind",
        "JJS": "Jack & Jones Smáralind",
        "SLS": "Selected Smáralind",
    }

# Create stores if not exist
for location_code, store_name in store_mapping.items():
    Store.objects.get_or_create(store_name=store_name)

# Process each record and populate models
for record in data:
    item_no = record["ItemNo"]
    variant_code = record["VariantCode"]
    location_code = record["LocationCode"]
    inventory_quantity = record["Inventory"]

    # Ensure the product exists
    product, _ = Product.objects.get_or_create(
        ItemNo=item_no,
        VariantCode=variant_code,
        defaults={"VariantName": "", "image_url": "", "noos": False}
    )

    # Get or create the store
    store_name = store_mapping.get(location_code, f"Store {location_code}")
    store, _ = Store.objects.get_or_create(store_name=store_name)

    # Create or update inventory
    Inventory.objects.update_or_create(
        store=store,
        product=product,
        defaults={"quantity": inventory_quantity}
    )

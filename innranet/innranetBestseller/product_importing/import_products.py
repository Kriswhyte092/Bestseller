import json
from models import Product, colorVariant, Variant, Store, Inventory
from api import bc_fetch_variant_stock, fc_fetch_product_json
from rich.console import Console

console = Console()


# Load the JSON file
def load_json(file_name):
    """
    Load JSON data from a file
    """
    with open(file_name, 'r') as file:
        return json.load(file)


def write_to_file(data, file_name):
    """
    Write data to a JSON file
    """
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

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

# Imports product details from a given object
def import_product(obj):
    product_name = obj.get('name', 'N/A') # Extract product name
    product_number = obj.get('number', 'N/A') # Extract product number
    
    # Create a Product instance
    product = Product(name=product_name, itemNo=product_number, noos=False)
    
    # Initialize a stack with the supplied object
    stack = [obj]
    # List to gather unique variants found in the object
    variants = []
    
    # Process stack items until empty
    while stack:
        current = stack.pop()
        # If current item is a dict, handle keys and values
        if isinstance(current, dict):
            for key, value in current.items():
                # For a list of color options
                if key == 'options' and isinstance(value, list):
                    for color_info in value:
                        color_code = color_info['number']
                        color_name = color_info['colors'][0]['name'][0]['text']
                        skus = []
                        images = []

                        # Create color variant for this product
                        color_variant = colorVariant(product=product, colorName=color_name, colorCode=color_code)
                        product.colorVariants.append(color_variant)

                        # Collect images if present
                        if color_info['media']['images']:
                            for image in color_info['media']['images']:
                                for url in image['urls']:
                                    images.append(url['url'])
                                    color_variant.image_urls.append(url['url'])

                        # Collect SKUs if present
                        if color_info['skus']:
                            for sku in color_info['skus']:
                                skus.append([sku['size'], sku['ean13']])
                                variants.append(str(sku['ean13'])[-6:])
                                
                                # Create variant object for each SKU
                                variant = Variant(colorVariant=color_variant, BarcodeNo=sku['ean13'], size=sku['size'])
                                color_variant.variant_details.append(variant)
                                
                                # debuging
                                console.print(variant)
                        # debuging
                        console.print(color_variant, style="blue")
                
                # Product description in Icelandic
                elif isinstance(value, list) and key == 'product_description':
                    for language in value:
                        if language['language'] == 'Icelandic':
                            product.product_description = language['text']
                    stack.append(value)
                else:
                    # Push any other dict/list entries for further inspection
                    stack.append(value)
        # If current item is a list, push its items to the stack
        elif isinstance(current, list):
            for item in current:
                stack.append(item)
    # Return the processed product and variants
    return product, variants 


## Product files
# product_12260628.json
# product_12260481.json
# product_12259664.json

# List of local product files
product_files = [
    "noos_products/product_12260628.json",
    "noos_products/product_12260481.json",
    "noos_products/product_12259664.json",
    "noos_products/product_12278009.json"
]
# Extract product data
# print the product data of each file in the product_files list
for product_file in product_files:
    data = load_json(product_file)
    p, v = import_product(data)
    console.print(p, style="purple")

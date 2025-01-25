import json
from models import Product, colorVariant, Variant, Store, Inventory
from api import bc_api_for_variant_stock, fashion_cloud_api
from rich.console import Console
import time

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
    Append data to a JSON file without overwriting existing content.
    """
    try:
        # Load existing data
        with open(file_name, "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, initialize an empty list
        existing_data = []

    # Convert the object to a dictionary if needed
    if hasattr(data, "to_dict"):
        data = data.to_dict()

    # Add the new data to the list
    existing_data.append(data)

    # Write the updated data back to the file
    with open(file_name, "w") as file:
        json.dump(existing_data, file, indent=4)


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
    product = Product(name=product_name, itemNo=product_number)
    
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

                        if color_info['noos_information']:
                            color_variant.noos = color_info['noos_information']['is_noos']
                            
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
                                #write_to_file(variant, "product_importing/JJ_noos_products.json")
                        # debuging
                        console.print(color_variant, style="blue")
                        #write_to_file(color_variant, "product_importing/JJ_noos_products.json")
                
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


# # List of local product files
# product_files = [
#     "noos_products/product_12260628.json",
#     "noos_products/product_12260481.json",
#     "noos_products/product_12259664.json",
#     "noos_products/product_12278009.json"
# ]
# # Extract product data
# # print the product data of each file in the product_files list
# for product_file in product_files:
#     data = load_json(product_file)
#     p, v = import_product(data)
#     console.print(p, style="purple")


"""
Short list of product codes,
use this list for testing purposes.
"""
product_codes = [
    "12260628",
    "12260481",
    "12259664",
]


"""
Use this list to fetch product data from all JJ noos products, 
else use the short list above for testing purposes.
"""
JJ_noos_barcodes = [
    "12230334", "12242998", "12136795", "12242690", "12152757",
    "12118114", "12263507", "12254346", "12206024", "12066296",
    "12059471", "12022977", "12269002", "12248067", "12111773",
    "12075392", "12248070", "12266069", "12262858", "12203642",
    "12240477", "12150724", "12217091", "12236089", "12209663",
    "12133074", "12147024", "12148275", "12259815", "12248551",
    "12168656", "12263530", "12263335", "12261690", "12111026",
    "12113450", "12278009", "12216664", "12193754", "12139912",
    "12141844", "12258150", "12193553", "12260907", "12150148",
    "12150160", "12150158", "12159954", "12200751", "12138115",
    "12227385", "12260628", "12182486", "12248409", "12266046",
    "12192150", "12097662", "12208157", "12259944", "12267470",
    "12259945", "12210830", "12270279", "12208364", "12189339",
    "12157417", "12157321", "12259666", "12259664", "12257479",
    "12265328", "12239460", "12268183", "12257492", "12265298",
    "12265315", "12182461", "12268609", "12258672", "12259449",
    "12259393", "12259459", "12260481", "12156101", "12254412",
    "12205777", "12113648", "12059220", "12200404", "12258848",
    "12156102", "12241611", "12251180", "12074784"
]

# 
start_time = time.time()

# Fetch product data from Fashion Cloud API
for code in product_codes:
    fashion_cloud_product = fashion_cloud_api(code)
    p, v = import_product(fashion_cloud_product)
    console.print(p, style="purple")
    #write_to_file(p, "product_importing/JJ_noos_products.json")

end_time = time.time()
console.print(f"Elapsed time: {end_time - start_time} seconds")
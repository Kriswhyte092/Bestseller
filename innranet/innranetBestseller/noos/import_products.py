import json
import logging
from tqdm import tqdm
from noos.models import Product, colorVariant, Variant, Store, Inventory
from noos.product_apis import bc_api_for_variant_stock, fashion_cloud_api

# Set up logging
logging.basicConfig(filename='log/import_products.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load the JSON file
def load_json(file_name):
    """
    Load JSON data from a file
    """
    with open(file_name, 'r') as file:
        return json.load(file)

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
def import_product(obj, code):
    """
    Extract product details from a nested object and return a Product instance.
    """
    try:
        if obj is None:
            print("\nError: Received None object\n")
            return None, None
        
        product_name = obj.get('name', 'N/A') # Extract product name
        product_number = obj.get('number', 'N/A') # Extract product number
        
        # Check if the product already exists
        product, created = Product.objects.get_or_create(itemNo=product_number, defaults={'name': product_name})
        
        if not created:
            # Update the existing product's name if it was found
            product.name = product_name
            product.save()
                
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
                            color_variant.save()  # Save the color variant to the database

                            # Collect images if present
                            if color_info['media']['images']:
                                for image in color_info['media']['images']:
                                    for url in image['urls']:
                                        images.append(url['url'])
                                        color_variant.image_urls.append(url['url'])
                                color_variant.save()  # Save the updated color variant

                            if color_info['noos_information']:
                                color_variant.noos = color_info['noos_information']['is_noos']
                                color_variant.save()  # Save the updated color variant
                            
                            # Collect SKUs if present
                            if color_info['skus']:
                                for sku in color_info['skus']:
                                    skus.append([sku['size'], sku['ean13']])
                                    variants.append(str(sku['ean13'])[-6:])
                                    
                                    # Create variant object for each SKU
                                    variant = Variant(colorVariant=color_variant, BarcodeNo=sku['ean13'], size=sku['size'])
                                    variant.save()  # Save the variant to the database
                                    
                                #     # Debugging
                                #     print(variant)
                                # # Debugging
                                # print(color_variant)
                                
                    # Product description in Icelandic
                    elif isinstance(value, list) and key == 'product_description':
                        for language in value:
                            if language['language'] == 'Icelandic':
                                product.product_description = language['text']
                                product.save()  # Save the updated product
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
    except Exception as e:
        logging.error(f"Error processing product: {code} - Error: {e}")
        return None, None


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


# # Fetch product data from Fashion Cloud API
# for code in tqdm(JJ_noos_barcodes, desc="Processing products"):
#     try:
#         fashion_cloud_product = fashion_cloud_api(code)
#         if fashion_cloud_product is None:
#             logging.error(f"Error fetching data for barcode: {code}")
#             continue
#         p, v = import_product(fashion_cloud_product, code)
#         print(p)
#     except Exception as e:
#         logging.error(f"Error processing barcode {code}: {e}")
#         continue
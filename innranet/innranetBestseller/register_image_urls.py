"""Kóði til að skrá image urls á product"""

import re
from noos.models import Product

# Read the image URLs from the file
with open('image_urls.txt', 'r') as f:
    urls = f.readlines()

# Dictionary to group URLs by ItemNo
item_urls = {}

for url in urls:
    try:
        # Extract ItemNo from the URL
        match = re.search(r'style/(\d+)/', url)
        if match:
            item_no = match.group(1)
            if item_no not in item_urls:
                item_urls[item_no] = []
            item_urls[item_no].append(url.strip())
        else:
            raise ValueError(f"ItemNo not found in URL: {url.strip()}")
    except Exception as e:
        print(f"Error processing URL '{url.strip()}': {e}")

# Update all products in the database with the same ItemNo
for item_no, urls in item_urls.items():
    try:
        products = Product.objects.filter(ItemNo=item_no)
        if products.exists():
            for product in products:
                # Append new URLs to existing ones
                product.image_urls = list(set(product.image_urls + urls))
                product.save()
        else:
            raise ValueError(f"No products found for ItemNo: {item_no}")
    except Exception as e:
        print(f"Error updating products for ItemNo '{item_no}': {e}")

print("Process completed.")

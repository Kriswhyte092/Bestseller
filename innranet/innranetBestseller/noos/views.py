import requests
from django.shortcuts import render
import json
import glob
import os

NOOS_FOLDER = "noos_products"

# Function to fetch and store JSON
def fetch_and_store_json(barcodes):

    base_url = "https://apigw.bestseller.com/pds/style/"
    headers = {"Ocp-Apim-Subscription-Key": "0d5c75bf70b244e6a7ab7480f6e39b07"}
    
    for barcode in barcodes:
        if os.path.exists(f"noos_products/product_{barcode}.json"):
            continue
        
        api_url = f"{base_url}{barcode}"
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            file_path = os.path.join(NOOS_FOLDER, f"product_{barcode}.json")

            # Save each product's data in a separate file
            with open(file_path, "w") as file:
                json.dump(response.json(), file, indent=4)
        except requests.RequestException as e:
            print(f"Error fetching data for barcode {barcode}: {e}")


def extract_image_urls(data, urls):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "images" and isinstance(value, list):
                for image in value:
                    if isinstance(image, dict) and "urls" in image:
                        urls.append(image["urls"][0]["url"])
            else:
                extract_image_urls(value, urls)
    elif isinstance(data, list):
        for item in data:
            extract_image_urls(item, urls)


def noos(request):
    barcodes = list(set([
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
    ])) # JJ NOOS barcodes
    fetch_and_store_json(barcodes)  # Fetch data for all barcodes

    products = []
    for product_data in load_all_products():
        # Extract product name and first image URL
        product_name = product_data.get("name", "No Name Available")
        image_urls = []
        extract_image_urls(product_data, image_urls)
        
        if image_urls:
            products.append({"name": product_name, "image_url": image_urls[0]})

    return render(request, "noos/noos.html", {"products": products})


def load_all_products():
    products = []
    for file_path in glob.glob("noos_products/product_*.json"):  # Match all product files
        try:
            with open(file_path, "r") as file:
                product_data = json.load(file)
                products.append(product_data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading or parsing file {file_path}: {e}")
    return products

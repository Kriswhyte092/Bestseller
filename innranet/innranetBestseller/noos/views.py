import requests
from django.shortcuts import render
import json

LOCAL_JSON_FILE = "product_data.json"

# Function to fetch and store JSON
def fetch_and_store_json():
    barcodes = ["5712836984809"]
    base_url = "https://apigw.bestseller.com/pds/style/ean/"
    headers = {
        "Ocp-Apim-Subscription-Key": "0d5c75bf70b244e6a7ab7480f6e39b07"
    }
    api_url = f'{base_url}{barcodes[0]}'
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(LOCAL_JSON_FILE, "w") as file:
            json.dump(response.json(), file, indent=4)
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return False
    return True

# Function to read JSON, extract data, and render
def product_info(request):
    # Ensure the JSON file exists (fetch if necessary)
    if not fetch_and_store_json():
        return render(request, 'noos/noos-info.html', {"name": "Error", "image_urls": []})
    
    try:
        with open(LOCAL_JSON_FILE, "r") as file:
            product_data = json.load(file)

        # Extract product name
        product_name = product_data.get("name", "No Name Available")

        # Extract image URLs
        images = product_data.get("media", {}).get("images", [])
        image_urls = []
        extract_image_urls(product_data, image_urls)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        product_name = "Error"
        image_urls = []

    context = {
        "name": product_name,
        "image_urls": image_urls
    }
    return render(request, 'noos/noos-info.html', context)

def extract_image_urls(data, urls):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'images' and isinstance(value, list):
                for image in value:
                    if isinstance(image, dict) and 'urls' in image:
                        urls.append(image['urls'][0]['url'])
                print(urls)
            else:
                extract_image_urls(value, urls)
    elif isinstance(data, list):
        for item in data:
            extract_image_urls(item, urls)
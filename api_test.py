import requests
import json
import re

# List of barcode numbers
barcodes = ["5712836984809"]

# Base URL
base_url = "https://apigw.bestseller.com/pds/style/ean/"

# Headers for the API request
headers = {
    "Ocp-Apim-Subscription-Key": "0d5c75bf70b244e6a7ab7480f6e39b07"
}

# Iterate over each barcode
for barcode in barcodes:
    # Construct the URL with the current barcode
    url = f"{base_url}{barcode}"
    
    # Send the GET request
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the product name
        product_number = str(data.get("number", f"output_{barcode}")
        )
        
        # Define the output file name based on the product number
        file_name = f"{product_number}.json"
        
        # Write the data to a JSON file
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4)  # Use indent for pretty printing
        
        print(f"Data for barcode {barcode} written to {file_name}")
    else:
        print(f"Error {response.status_code} for barcode {barcode}")


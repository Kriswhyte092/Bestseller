import requests
import json


def bc_api_for_variant_stock():
    """
    Fetches product stock data from Bestseller API
    """
    
    base_url = "https://bc.bestseller.is:7948/Bestseller-DEV/ODataV4/Company('VM')/variantloc?$select=ItemNo,VariantCode,LocationCode,Inventory,barcodeNo"
    headers = {"Authorization": "Basic S1JJU1RPRkVSOkthZmZpS2V4T2dQaXBhcjEzIQ=="}
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def fashion_cloud_api(number):
    """
    Takes in a products ItemNo and fetches the product data from Fashion Cloud API
    """
    
    base_url = "https://apigw.bestseller.com/pds/style/"
    headers = {"Ocp-Apim-Subscription-Key": "0d5c75bf70b244e6a7ab7480f6e39b07"}
    api_url = f"{base_url}{number}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

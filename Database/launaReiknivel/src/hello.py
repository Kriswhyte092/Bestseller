import requests
import psycopg2
from datetime import datetime

# Constants
API_URL = "https://api.getsling.com/v1/personas"
API_KEY = "413c2a4da28c4e85ae19bca831afdb45"

def fetch_employees():
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return []


def main():
    employees = fetch_employees()
    for employee in employees:

    # fetchar employees frá API



if __name__ == "__main__":
    main()

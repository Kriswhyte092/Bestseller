import requests
from datetime import datetime


def fetch_shifts(url, key):
    # dags. format
    #yyyy-mm-ddT00:01:00Z/yyyy-mm-ddT23:59:00Z
    #dates = get_dates()
    dates = "2024-12-21/2025-01-20"
    url = f"{url}/reports/timesheets?dates={dates}"

    headers = {
        "Authorization": key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"eih kluðraðist fifl {response.status_code} {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"þu ert halfviti {e}")
        return None

#við viljum fá dagsetningar frá 21. -> 20. næsta mán.
def get_dates():
    month_curr = datetime.now().month
    year_curr = datetime.now().year
    
    if month_curr == 1:  # Janúar
        return f"{year_curr-1}-12-21T00:01:00Z/{year_curr}-01-20T23:59:00Z"
    else:
        prev_month = f"{month_curr-1:02}"
        curr_month = f"{month_curr:02}"
        return f"{year_curr}-{prev_month}-21T00:01:00Z/{year_curr}-{curr_month}-20T23:59:00Z"


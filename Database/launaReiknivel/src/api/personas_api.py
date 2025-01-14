import requests


def fetch_personas(url, key):
    url = f"{url}/personas"

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

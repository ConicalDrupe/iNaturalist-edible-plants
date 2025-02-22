import pandas as pd
import json
import requests
import os

def match(name):
    url = "https://api.gbif.org/v1/species/match"

    params = {
        "name":name,
        "rank": "SPECIES",
        "kingdom":"Plantae",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200 or 201:
        data = json.loads(response.text)
    else:
        print(f"Error: {response.status_code}")
        return

    return data

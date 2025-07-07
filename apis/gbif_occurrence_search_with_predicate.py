import os
import requests
import json
import gbif_password as g
from pprint import pprint

url = "https://api.gbif.org/v1/occurrence/search/predicate"

def search(predicate_path):
    with open(predicate_path) as f:
        data = f.read()
        # data = f.read().replace('\n', '').replace('\r', '').encode()
        # pprint(data)

    headers = {'Content-Type' : 'application/json'}

    response = requests.post(url, data=data, headers=headers, auth=(g.user,g.p))

    if response.status_code == 200 or 201:
        data = json.loads(response.text)
        return data
    else:
        print(f"Error: {response.status_code}")
        return

if __name__ == "__main__":
    predicate = '/home/boon/Projects/iNaturalist-edible-plants/outputs/650all_taxonKeys_query.json'
    result = search(predicate)
    print('Total Number of Occurances found: ',result["count"])
    # pprint(result["results"])

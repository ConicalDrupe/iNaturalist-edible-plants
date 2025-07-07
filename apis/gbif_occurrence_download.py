import requests
import json
import gbif_password as g

# iNaturalist dataset key  50c9509d-22c7-4a22-a47d-8c48425ef4a7

#Download dataset
def download(predicate_path):
    url = "https://api.gbif.org/v1/occurrence/download/request"
    with open(predicate_path) as f:
        data = f.read()

    headers = {'Content-Type' : 'application/json'}

    response = requests.post(url, data=data, headers=headers, auth=(g.user,g.p))

    if response.status_code == 200 or 201:
        print('[DOWNLOAD KEY]')
        print(response.text)
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return

if __name__ == '__main__':
    # download('/home/ubuntu/iNaturalist-edible-plants/outputs/317_taxonKeys_query.json')
    download('/home/boon/Projects/iNaturalist-edible-plants/outputs/650all_taxonKeys_query.json')

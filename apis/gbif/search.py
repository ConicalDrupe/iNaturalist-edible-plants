import requests
import json
import gbif_password as g

url = "https://api.gbif.org/v1/occurrence/search/predicate"
with open('query.json') as f:
    data = f.read()
    # data = f.read().replace('\n', '').replace('\r', '').encode()

headers = {'Content-Type' : 'application/json'}

response = requests.post(url, data=data, headers=headers, auth=(g.user,g.p))

if response.status_code == 200 or 201:
    print(response.text)
    print('-'*10)
    print(f"Status Code: {response.status_code}")
else:
    print(f"Error: {response.status_code}")
    

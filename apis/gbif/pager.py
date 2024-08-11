import requests
import gbif_password as g

# Implement Pager to request queries, in 100 intervals.
# Reads queries from createQuery.py

url = "https://api.gbif.org/v1/occurrence/download/request"
with open('query.json') as f:
    data = f.read()
    # data = f.read().replace('\n', '').replace('\r', '').encode()

headers = {'Content-Type' : 'application/json'}

response = requests.post(url, data=data, headers=headers, auth=(g.user,g.p))

if response.status_code == 200 or 201:
    print('[DOWNLOAD KEY]')
    print(response.text)
    print('-'*10)
    print(f"Status Code: {response.status_code}")
else:
    print(f"Error: {response.status_code}")
    

import requests
from gbif_password import user,pass

# https://api.gbif.org/v1/
# https://api.gbif.org/v1/occurence/search?

#   Georgia polygon boarder:
#   https://gist.github.com/JoshuaCarroll/49630cbeeb254a49986e939a26672e9c

# iNaturalist dataset key  50c9509d-22c7-4a22-a47d-8c48425ef4a7

#Download dataset
url = "https://api.gbif.org/v1/occurrence/download/request"
with open('query.json') as f:
    data = f.read().replace('\n', '').replace('\r', '').encode()

headers = {'Content-Type' : 'application/json'}

response = requests.post(url, data=data, headers=headers, auth=(user,pass))

if response.status_code == 200 or 201:
    print('[DOWNLOAD KEY]')
    print(response.text)
    print('-'*10)
else:
    print(f"Error: {response.status_code}")
    
#%%
# take download_key = json.loads(response.text)
# check download status every 10-15 min
# and automatically download data once download is complete
# load data into python with pandas
# clean
# insert into sql database


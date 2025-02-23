import pandas as pd
import json
import requests
import datetime
import gbif_password as g
import os

def match(name):
    url = "https://api.gbif.org/v1/species/match"

    params = {
        "name":name,
        "rank": "SPECIES",
        "kingdom":"Plantae",
    }

    response = requests.get(url, params=params,auth=(g.user,g.p))

    if response.status_code == 200 or 201:
        data = json.loads(response.text)
    else:
        print(f"Error: {response.status_code}")
        return

    return data

def match_all(names):

    all_records = []

    for name in names:
        data = match(name)

        if data:
            record = {
                'searchedName':name, # will use to match back to our input file
                'canonicalName':data['canonicalName'],
                'scientificName':data['scientificName'],
                'rank':data['rank'],
                'usageKey':data['usageKey'],
                # 'family':data['family'],
                'match_confidence':data['confidence'],
                'matchType':data['matchType']
            }
            all_records.append(record)

    return all_records

def save_matches(record_ls,save_path):
    # Expects a list of dictionaries
    df = pd.DataFrame(record_ls)


    df.to_csv(save_path,index=False)
    print(f'[INFO] Saved matched names to {save_path}')
    return True

def run_match_service(file_to_match='/home/ubuntu/iNaturalist-edible-plants/bookscraping/cleaning/edible_wild_IM.csv',save_dir='/home/ubuntu/iNaturalist-edible-plants/outputs'):
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%Y-%m-%d_%H-%M-%S")

    df = pd.read_csv(file_to_match)

    scientificName_ls = df["scientific_name"].to_list()
    print('Number of scientific names:',len(scientificName_ls))

    save_path = os.path.join(save_dir,f'gbif_search_service_output_{len(scientificName_ls)}_{timestamp}.csv')
    all_records = match_all(scientificName_ls)
    print("Saving file...\nfile:\n",save_path)
    save_matches(all_records,save_path)
    return save_path

if __name__ == '__main__':
    run_match_service()

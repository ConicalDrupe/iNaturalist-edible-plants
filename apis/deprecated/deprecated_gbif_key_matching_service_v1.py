import pandas as pd
import json
import argparse
import requests
import datetime
import gbif_password as g
import os

parser = argparse.ArgumentParser(prog='GBIF Key Matching Service',
                                 description='Matches Scientific Names to GBIF usage keys')

parser.add_argument('-s','--species',help='Species Rank',action=argparse.BooleanOptionalAction)
parser.add_argument('-g','--genus',help='Genus Rank',action=argparse.BooleanOptionalAction)
parser.add_argument('-a','--all',help='Run all as Species Rank',action=argparse.BooleanOptionalAction)

args = parser.parse_args()

def match(name):
    url = "https://api.gbif.org/v1/species/match"

    if args.species or args.all:
        params = {
            "name":name,
            "rank": "SPECIES",
            "kingdom":"Plantae",
        }
    elif args.genus:
        params = {
            "name":name,
            "rank": "GENUS",
            "kingdom":"Plantae",
        }
    else:
        print('-s or -g or -a flag required')
        exit()

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

def run_match_service(file_to_match='/home/boon/Projects/iNaturalist-edible-plants/bookscraping/outputs/reprocessing/final_665_species.csv',save_dir='/home/boon/Projects/iNaturalist-edible-plants/outputs',name_col='name'):
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%Y-%m-%d_%H-%M-%S")

    df = pd.read_csv(file_to_match)

    # Arg parser
    df['name_len'] = df[name_col].apply(lambda x: len(x.split(' ')))
    if args.species:
        df = df[df['name_len']>=2]
        file_flag='species'
    elif args.genus:
        df = df[df['name_len']==1]
        file_flag='genus'
    elif args.all:
        file_flag='all'
    else:
        print('-s or -g flag required')
        exit()

    scientificName_ls = df[name_col].to_list()
    print('Number of scientific names:',len(scientificName_ls))

    save_path = os.path.join(save_dir,f'gbif_search_service_output_{len(scientificName_ls)}_{file_flag}_{timestamp}.csv')
    all_records = match_all(scientificName_ls)
    save_matches(all_records,save_path)
    return save_path

if __name__ == '__main__':
    run_match_service()

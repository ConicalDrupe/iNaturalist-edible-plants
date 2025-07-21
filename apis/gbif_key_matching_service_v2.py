import pandas as pd
import json
import argparse
import requests
import datetime
import gbif_password as g
import os
from pprint import pprint

parser = argparse.ArgumentParser(prog='GBIF Key Matching Service',
                                 description='Matches Scientific Names to GBIF usage keys')

parser.add_argument('-s','--species',help='Species Rank',action=argparse.BooleanOptionalAction)
parser.add_argument('-g','--genus',help='Genus Rank',action=argparse.BooleanOptionalAction)
parser.add_argument('-a','--all',help='Run all as Species Rank',action=argparse.BooleanOptionalAction)

parser.add_argument('-f','--file',help='Absolute Path to csv file')

args = parser.parse_args()

def match(name):
    url = "https://api.gbif.org/v2/species/match"

    if args.species or args.all:
        params = {
            "scientificName":name,
            "taxonRank": "SPECIES",
            "kingdom":"Plantae",
        }
    elif args.genus:
        params = {
            "scientificName":name,
            "taxonRank": "GENUS",
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

def parse_v2_response(data,name):
    family=''
    family_key=''
    genus=''
    genus_key=''
    species=''
    species_key=''
    for item in data['classification']:
        key = item['key']
        n = item['name']
        rank = item['rank']

        if rank == 'FAMILY':
            family = n
            family_key = key
        elif rank == 'GENUS':
            genus = n
            genus_key = key
        elif rank == 'SPECIES':
            species = n
            species_key = key
        else:
            continue

    diagnostics = data['diagnostics']
    usage = data['usage']

    parsed_data = {
        'searchedName':name,
        'usageKey':usage['key'],
        'canonicalName':usage['canonicalName'],
        'formattedName':usage['formattedName'], # scientific name between <i> </i> tags
        'rank':usage['rank'],
        'family':family,
        'family_key':family_key,
        'genus':genus,
        'genus_key':genus_key,
        'species':species,
        'species_key':species_key,
        'confidence':diagnostics['confidence'],
        'matchType':diagnostics['matchType'],
    }

    return parsed_data

def match_all(names):

    all_records = []

    for name in names:
        data = match(name)

        if data:
            record = parse_v2_response(data,name)
            all_records.append(record)

    return all_records

def save_matches(record_ls,save_path):
    # Expects a list of dictionaries
    df = pd.DataFrame(record_ls)


    df.to_csv(save_path,index=False)
    print(f'[INFO] Saved matched names to {save_path}')
    return True

def run_match_service(save_dir='/home/boon/Projects/iNaturalist-edible-plants/apis/outputs',name_col='name'):

    if args.file:
        file_to_match = args.file
        df = pd.read_csv(file_to_match)
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
    elif list_of_names:
        file_flag='fromList'
        scientificName_ls = list_of_names.copy()
    else:
        print('-f or argument is required OR list of names.')
        exit()

    dt = datetime.datetime.now()
    timestamp = dt.strftime("%Y-%m-%d_%H-%M-%S")

    print('Number of scientific names:',len(scientificName_ls))

    save_path = os.path.join(save_dir,f'gbif_search_service_output_{len(scientificName_ls)}_{file_flag}_{timestamp}.csv')
    all_records = match_all(scientificName_ls)
    save_matches(all_records,save_path)
    return save_path

def test_match():
    name = 'Salicornia glasswort' #purposefuly typo
    data = match(name)
    pprint(data)
    print('\n\n\n')
    parsed = parse_v2_response(data,name)
    pprint(parsed)
    return

def test_species_match_all():
    list_of_names = ['Salicornia glasswort','']
    run_match_service()
    return

def test_genus_match_all():
    run_match_service()
    return

### WRITE A FUNCTION THAT ACTS AS A GENUS/SPECIES SWITCH!
# If the number of words in the input species_name ==1: match on genus. If == 2 search on species
if __name__ == '__main__':
    run_match_service()

    # # Testing option
    # list_of_names = ['Allium','Acer','Quercus']
    # test_genus_match_all()


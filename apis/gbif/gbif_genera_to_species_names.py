
import os
import pandas as pd
import requests
import json

def helper_contains_nubKey(pages):
    # A paging function that searches for 'nubKey' key
    for index,page in enumerate(pages):
        if "nubKey" in page:
            return index
        else:
            continue
    print('[ERROR] nubKey not found in any pages')
    return False



genera = ['Angelica', 'Malus', 'Vaccinium',
          'Solidago', 'Ribes', 'Smilax',
          'Crataegus', 'Carya', 'Amelanchier',
          'Quercus', 'Plantago', 'Rosa',
          'Rhus', 'Viola', 'Vitis', 'Lactuca']

searchLimit = 10

for name in genera:
    print(f'[INFO] Genera: {name}')

    # nubKey is GBIF Backbone key? 
    # dataset_Id is iNaturalist research grade observations 
    url = "https://api.gbif.org/v1/species/search"
    generaKey = []

    params = {
        "dataset_Id" : "50c9509d-22c7-4a22-a47d-8c48425ef4a7",
        "q" : name,
        "rank" : 'GENUS',
        "limit" : searchLimit
    }

    response = requests.get(url, params=params)

    if response.status_code == 200 or 201:
        data = json.loads(response.text)

        result = data["results"]

        # Paging through result, to find first nubKey
        index = helper_contains_nubKey(result)
        print('Index type',type(index))
        if type(index) == int:
            genera = {
            "name" : result[index]["scientificName"],
            "nubKey" : result[index]["nubKey"],
            "rank" : result[index]["rank"]
            }
        else:
            print(f'[No nubKey found] Error with {name}')
            break

        # for i, pageCurr in enumerate(result):
        #     if "nubKey" in pageCurr:
        #         print("nubKey found!")
        #         print(f"found in list index: {i}")
        #         printme = json.dumps(pageCurr,indent=4)
        #         print(printme)
        #
        #         genera = {
        #         "name" : pageCurr["scientificName"],
        #         "nubKey" : pageCurr["nubKey"],
        #         "rank" : pageCurr["rank"]
        #         }
        #         break

        # data_str = json.dumps(genera,indent=4)
        # print(data_str)
    else:
        print(f"Error: {response.status_code}")
        print(f'[First API Call] Error with {name}')
        break

    ## Second API call -> using nubkey to gt species
    params_2 = {
        "dataset_Id" : "50c9509d-22c7-4a22-a47d-8c48425ef4a7",
        "higherTaxonKey" : genera["nubKey"],
        "rank": 'SPECIES',
        "limit" : 500
    }

    response_2 = requests.get(url, params = params_2)

    if response_2.status_code == 200 or 201:
        data2 = json.loads(response_2.text)
        # species_txt = json.dump(species,indent=4)
        # print(species_text)
    else:
        print(f"Error: {response_2.status_code}")
        print(f'[Second API Call] Error with {name}')
        break

    ## Paging through results and saving:

    species_list = []

    result2 = data2["results"]
    for page in result2:
        if 'nubKey' not in page:
            continue
        else:
          species = { 'nubKey' : page['nubKey'],
                     'Genus' : page['genus'],
                     'Species Name': page['species']
                     }
          species_list.append(species)

    ## Saving results of a single Genera
    df = pd.DataFrame.from_records(species_list,index=range(0,len(species_list)))
    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    two_dir_back = os.path.normpath(back_dir + os.sep + os.pardir)
    df.to_csv(os.path.join(two_dir_back,'data','outputs','api',f'{name}_speciesList.csv'),index=False)

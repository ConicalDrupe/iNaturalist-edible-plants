import requests
import json
#import pprint
# 134847080
# 179049462
# nubKey is species_key

url = "https://api.gbif.org/v1/species/search"

test_names = [
            "Sambucus canadensis",
            "Morus rubra",
            "Laportea canadensis",
            "Juglans nigra",
            "Asclepias syriaca",
            "Achillea millefolium",
            "Opuntia humifusa",
            "Callicarpa americana"
          ]

# to-do next:
    # for high volume search, introduce random delay between requests
    # and header randomization
def get_species_keys(names, limit=3):
    # dataset_Id is iNaturalist research grade observations 
    url = "https://api.gbif.org/v1/species/search"
    species_keys = []

    for name in names:
        params = {
            "dataset_Id" : "50c9509d-22c7-4a22-a47d-8c48425ef4a7",
            "q" : name,
            "limit" : limit
        }

        ## insert random delay here

        ##
        print(f"searching species_key for: {name}")
        response = requests.get(url, params=params)

        if response.status_code == 200 or 201:
            data = json.loads(response.text)
        else:
            print(f"Error: {response.status_code}")
            break

        temp = data["results"]
        # iterate through results dic to find nubKey 
        # (speciesKey in gbif)
        for i, res in enumerate(temp):
            temp_l = temp[i]
            if "nubKey" in temp_l:
                speciesKey = temp_l["nubKey"]
                print("nubKey found!")
                print(f"found in list index: {i}")
                break
        
        species_keys.append(speciesKey)
    
    print("Key search of species done!")
    return species_keys


if __name__ == "__main__":
    import requests
    import json
    import pandas as pd

    path = '/home/boon/Projects/iNaturalist-edible-plants/data/outputs/southeast-foraging-rawdata.csv'
    df = pd.read_csv(path)

    # count blank spaces (single worded rows have zero spaces)
    print('[UNIQUE SPECIES] Before mask:', df["Scientific Name"].nunique())
    mask = df["Scientific Name"].str.count(' ') == 1
    df2 = df.loc[mask] 
    print('[UNIQUE SPECIES] After mask :', df2["Scientific Name"].nunique())

    species_list = df2["Scientific Name"].to_list()
    print(species_list)

    # species_keys = get_species_keys(species_list)

    ## save 100 species and keys to file
    # df_keys = pd.DataFrame()
    # df_keys['Species'] = species_list
    # df_keys['GBIF NubKey'] = species_keys
    #
    # save_path = '/home/boon/Projects/iNaturalist-edible-plants/data/outputs/gbif_species_keys.csv'
    # df_keys.to_csv(save_path)

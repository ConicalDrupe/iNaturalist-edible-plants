import pandas as pd
import json
import os
import numpy as np

# class snippet source: 
# https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def createQuery(taxon_key_list,save_dir='/home/boon/Projects/iNaturalist-edible-plants/outputs',template_path='/home/boon/Projects/iNaturalist-edible-plants/apis/inat_usa_predicate_template.json',name_flag=""):
    """
    Create a Json Header Parameter, with nubKey list no larger 100,000 for GBIF query request.
    """

    with open(template_path,'r') as j:
        template = json.load(j) # load for file format, loads for strring format

    template['predicate']['predicates'][1]['values'] = taxon_key_list

    print(type(template['predicate']['predicates'][1]['values']))

    save_path = os.path.join(save_dir,f'{len(taxon_key_list)}{name_flag}_taxonKeys_query.json')
    with open(save_path,'w') as new_json:
        json.dump(template,new_json,cls=NpEncoder)

    return save_path

if __name__ == '__main__':
    # df = pd.read_csv('/home/ubuntu/iNaturalist-edible-plants/outputs/gbif_search_service_output_317_2025-02-23_03-39-18.csv')
    # print(df.columns)
    df = pd.read_csv('/home/boon/Projects/iNaturalist-edible-plants/outputs/gbif_search_service_output_665_all_2025-07-05_18-58-49.csv')
    # Supressing kingdom observations
    df = df[df['rank']!='KINGDOM']
    
    taxon_key_ls = df['usageKey'].unique()
    print(f'Dataframe has {df.shape[0]} rows')
    print(f'Number of unique keys found: {len(taxon_key_ls)}')
    save_path = createQuery(taxon_key_ls,name_flag='all')
    print('Predicate saved at: ',save_path)

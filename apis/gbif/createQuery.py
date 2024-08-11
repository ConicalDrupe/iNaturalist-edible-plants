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

def createQuery(index):
    """
    Create a Json Header Parameter, with nubKey list no larger 100, for GBIF query request.
    """
    template_path = os.path.join(os.getcwd(),'template.json')

    back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    two_back_dir = os.path.normpath(back_dir + os.sep + os.pardir)
    compiled_species_ids = os.path.join(two_back_dir,'data','outputs','all_genera_to_species.csv')

    df = pd.read_csv(compiled_species_ids)
    species_keys = list(df['nubKey'].unique())

    length=0
    numSplits = np.ceil(df['nubKey'].nunique()/ 100)
    splits = np.array_split(df, numSplits)
    print(len(splits))
    for split in splits:
        print(split)
        print(type(split))
        break
    #
    #
    #     with open(template_path,'r') as j:
    #         template = json.load(j) # load for file format, loads for strring format
    #
    #     template['predicate']['predicates'][1]['values'] = split.to_list()
    #
    # # print(type(template['predicate']['predicates'][1]['values']))
    #
    with open(f'{index}_query.json','w') as new_json:
        json.dump(template,new_json,cls=NpEncoder)

if __name__ == '__main__':
    createQuery(0)
